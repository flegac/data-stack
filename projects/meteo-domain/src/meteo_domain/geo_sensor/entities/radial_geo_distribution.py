from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RadialGeoDistribution:
    scale: float = 1.0
    variance_ratio: float = 0.0

    def normal(self, center: tuple[float, float], n: int) -> np.ndarray:
        return np.random.normal(loc=center, scale=self.scale, size=(n, 2))
