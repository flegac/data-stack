from abc import ABC, abstractmethod
from typing import Generator, Any

from meteo_measures.domain.entities.measures.measure_series import MeasureSeries


class MeasureReader(ABC):

    @abstractmethod
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        ...
