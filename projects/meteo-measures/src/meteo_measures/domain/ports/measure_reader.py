from abc import ABC, abstractmethod
from typing import Any, Generator

from meteo_measures.domain.entities.measures.measure_series import MeasureSeries


class MeasureReader(ABC):
    @abstractmethod
    def read_all(self) -> Generator[MeasureSeries, Any, None]: ...
