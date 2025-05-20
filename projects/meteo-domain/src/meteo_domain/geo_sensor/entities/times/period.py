from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np

from meteo_domain.geo_sensor.entities.times.times import Times

MIN_SPLIT_SIZE = 2


@dataclass(frozen=True)
class Period:
    start: datetime | None = None
    end: datetime | None = None

    @staticmethod
    def from_duration(start: datetime, duration: timedelta):
        return Period(start, start + duration)

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def split(self, n: int):
        assert n >= MIN_SPLIT_SIZE
        delta = self.duration / (n - 1)
        raw = np.array([self.start + i * delta for i in range(n)], dtype="datetime64")
        return Times.from_raw(raw)
