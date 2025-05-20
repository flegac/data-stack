from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import euclidean


@dataclass(frozen=True)
class RadialValueDistribution:
    center: tuple[float, float]
    value: float = 1.0
    scale: float = 1.0
    variance_ratio: float = 0.0

    def compute_value(self, point: tuple[float, float]):
        distortion = 1 + np.random.rand() * self.variance_ratio
        dist = euclidean(self.center, point) / self.scale
        expected_value = self.value / (1.0 + dist**2)
        res = distortion * expected_value
        return res
