import random
from pathlib import Path

import cv2
import numpy as np
from easy_kit import timing
from scipy.spatial.distance import euclidean

from meteo_domain.geo_sensor.entities.location.location import Location
from meteo_domain.geo_sensor.entities.radial_geo_distribution import (
    RadialGeoDistribution,
)
from meteo_domain.geo_sensor.entities.radial_value_distribution import (
    RadialValueDistribution,
)
from meteo_domain.geo_sensor.generator import Generator
from meteo_domain.geo_sensor.heatmap_service import HeatmapService
from meteo_domain.geo_sensor.sensor_service import SensorService

POINT_RADIUS = 1
OUTPUT_PATH = Path.cwd() / "output"


def draw_image(heatmap, points, size):
    # Convertir les points en coordonnées entières pour le dessin
    points_int = (points * size).astype(np.int32)

    # Créer une image vide pour dessiner les points
    image_with_points = heatmap.copy()
    for point in points_int:
        # Inverser les coordonnées y pour correspondre à l'échelle de l'image OpenCV
        cv2.circle(image_with_points, (point[1], point[0]), POINT_RADIUS, (0, 0, 0), -1)

    return image_with_points


def main(seed: int):
    np.random.seed(seed)
    sensor_service = SensorService()
    heatmap_service = HeatmapService()

    with timing.timing("generate centroids"):
        root = Location.from_raw((0.0, 0.0))
        root_distribution = RadialGeoDistribution(scale=1.0, variance_ratio=0.1)
        root_value_distribution = RadialValueDistribution(
            center=root.raw, scale=1.0, variance_ratio=0.1
        )

        generators = [
            Generator(
                geo=RadialGeoDistribution(
                    scale=0.05,
                ),
                value=RadialValueDistribution(
                    center=center,
                    scale=0.05,  # + 0.2 * np.random.rand(),
                    value=euclidean(center, root.raw) ** 1.2
                    * root_value_distribution.compute_value(center)
                    * (1 + 4 * np.random.rand()),
                ),
            )
            for center in root_distribution.normal(root.raw, 1_000)
        ]
    with timing.timing("generate measurements"):
        measurements = []
        for generator in generators:
            measurements.extend(sensor_service.fake_measurements2(generator, 100))

    heatmap = heatmap_service.compute_heatmap(measurements, min_distance=0.001)

    # Sauvegarder l'image dans un fichier

    output_file = OUTPUT_PATH / f"heatmap_{seed}.png"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_file), heatmap)

    print(f"L'image a été sauvegardée dans {output_file}")


if __name__ == "__main__":
    timing.setup_timing()
    for _ in range(2):
        seed = random.randint(0, 10000)
        main(seed)
