from dataclasses import dataclass

import numpy as np

from meteo_domain.geo_sensor.entities.location.location import Location

LOCATION_POINT_SIZE = 2
LOCATION_NDIM = 2


@dataclass(frozen=True)
class Locations:
    raw: np.ndarray

    @staticmethod
    def from_raw(raw: np.ndarray):
        assert raw.dtype == np.float64
        assert raw.ndim == LOCATION_NDIM
        assert raw.shape[1] == LOCATION_POINT_SIZE
        return Locations(raw)

    @property
    def size(self):
        return self.raw.shape[0]

    @property
    def latitudes(self):
        return self.raw[:, 1]

    @property
    def longitudes(self):
        return self.raw[:, 0]

    def iter(self):
        for row in self.raw:
            yield Location.from_raw(row)
