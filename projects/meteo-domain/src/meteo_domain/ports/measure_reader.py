from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any

from meteo_domain.entities.measures.measure_series import MeasureSeries


class MeasureReader(ABC):
    @abstractmethod
    def read_all(self) -> Generator[MeasureSeries, Any, None]: ...
