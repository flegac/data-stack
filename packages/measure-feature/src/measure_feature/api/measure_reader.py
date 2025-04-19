from abc import ABC, abstractmethod
from typing import Generator, Any

from measure_feature import MeasureQuery, MeasureSeries


class MeasureReader(ABC):

    @abstractmethod
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        ...

    @abstractmethod
    def search(self, query: MeasureQuery) -> MeasureSeries:
        ...
