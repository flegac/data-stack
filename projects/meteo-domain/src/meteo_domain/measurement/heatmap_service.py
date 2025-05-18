import cv2
import numpy as np
from easy_kit.timing import time_func
from scipy.interpolate import griddata

from meteo_domain.measurement.entities.measurement import TaggedMeasurement
from meteo_domain.measurement.poisson_disk_sampling import (
    poisson_disk_sampling,
)

OUTPUT_SIZE = 2048


class HeatmapService:
    def poisson_disc_sampling(
        self,
        measurements: list[TaggedMeasurement],
        min_distance: float = 0.01,
    ):
        points = np.array(
            [
                (_.sensor.location.longitude, _.sensor.location.latitude)
                for _ in measurements
            ]
        )
        normalized_points = normalize(points)
        sampled_indices = poisson_disk_sampling(normalized_points, min_distance)
        return [points[_] for _ in sampled_indices]

    def compute_heatmap(
        self,
        measurements: list[TaggedMeasurement],
        min_distance: float = 0.01,
    ):
        points = np.array(
            [
                (_.sensor.location.longitude, _.sensor.location.latitude)
                for _ in measurements
            ]
        )
        values = np.array([_.value for _ in measurements])
        normalized_points = normalize(points)
        sampled_indices = poisson_disk_sampling(normalized_points, min_distance)
        sampled_points = np.array([points[_] for _ in sampled_indices])
        sampled_values = np.array([values[_] for _ in sampled_indices])
        sampled_points = normalize(sampled_points)
        heatmap = compute_heatmap(sampled_points, sampled_values, OUTPUT_SIZE)
        return heatmap


def normalize(points: np.ndarray):
    min_vals = np.min(points, axis=0)
    max_vals = np.max(points, axis=0)
    return (points - min_vals) / (max_vals - min_vals)


@time_func
def compute_heatmap(points, values, size: int):
    grid_x, grid_y = np.mgrid[0 : 1 : size * 1j, 0 : 1 : size * 1j]

    # Interpoler les données
    interpolated_values = griddata(
        points, values, (grid_x, grid_y), method="cubic", fill_value=-1
    )

    # Normaliser les valeurs interpolées pour qu'elles soient entre 0 et 255
    interpolated_values_normalized = (
        (interpolated_values - interpolated_values.min())
        / (interpolated_values.max() - interpolated_values.min())
        * 255
    )
    interpolated_values_normalized = interpolated_values_normalized.astype(np.uint8)

    # Appliquer une colormap pour la visualisation
    heatmap = cv2.applyColorMap(interpolated_values_normalized, cv2.COLORMAP_VIRIDIS)

    return heatmap
