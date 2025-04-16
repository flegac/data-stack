from abc import ABC, abstractmethod

from measure_feature import MeasureQuery, MeasureSeries


class MeasureReader(ABC):
    @abstractmethod
    def search(self, query: MeasureQuery) -> MeasureSeries:
        ...
