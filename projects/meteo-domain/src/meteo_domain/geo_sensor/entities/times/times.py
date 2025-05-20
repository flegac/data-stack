import datetime
from dataclasses import dataclass

import numpy as np
from easy_kit.timing import time_func

from meteo_domain.core.dates import to_datetime


@dataclass(frozen=True)
class Times:
    raw: np.ndarray

    @staticmethod
    def merge(items: list["Times"]):
        return Times.from_raw(np.concatenate([_.raw for _ in items], axis=0))

    @staticmethod
    def from_raw(raw: np.ndarray):
        assert raw.ndim == 1
        assert raw.dtype == "datetime64[us]"
        return Times(raw)

    @property
    def size(self):
        return self.raw.shape[0]

    @time_func
    def read(self, idx: int) -> datetime.datetime:
        return to_datetime(self.raw[idx])

    def __iter__(self):
        for _ in range(self.size):
            yield self.read(_)
