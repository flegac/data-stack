import random
from pathlib import Path

import cv2
import numpy as np
from easy_kit import timing
from scipy.spatial.distance import euclidean

from meteo_domain.measurement.centroid import Centroid
from meteo_domain.measurement.heatmap_service import HeatmapService
from meteo_domain.measurement.measurement_service import MeasurementService

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
    measurement_service = MeasurementService()
    heatmap_service = HeatmapService()

    with timing.timing("generate centroids"):
        root = Centroid(
            center=(0.0, 0.0),
            scale=1.0,
            size=1000,
            variance_ratio=0.1,
        )
        centroids = [
            Centroid(
                center=center,
                scale=0.05,  # + 0.2 * np.random.rand(),
                size=100,
                value=euclidean(center, root.center) ** 1.2
                * root.compute_value(center)
                * (1 + 4 * np.random.rand()),
            )
            for center in root.generate_random_points()
        ]
    with timing.timing("generate measurements"):
        measurements = []
        for centroid in centroids:
            measurements.extend(measurement_service.randomize(centroid))

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
