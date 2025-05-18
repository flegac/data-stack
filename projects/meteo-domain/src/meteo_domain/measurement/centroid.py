from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import euclidean


@dataclass
class Centroid:
    size: int
    center: tuple[float, float]
    scale: float = 1.0
    value: float = 1.0
    variance_ratio: float = 0.0

    def generate_random_points(self):
        return np.random.normal(loc=self.center, scale=self.scale, size=(self.size, 2))

    def compute_value(self, point: tuple[float, float]):
        distortion = 1 + np.random.rand() * self.variance_ratio
        dist = euclidean(self.center, point) / self.scale
        expected_value = self.value / (1.0 + dist**2)
        res = distortion * expected_value
        return res
