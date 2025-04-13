from abc import ABC, abstractmethod

from measure_repository import Measure, MeasureQuery, MeasureSeries


class MeasureRepository(ABC):

    @abstractmethod
    def write(self, measure: Measure):
        ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        ...

    @abstractmethod
    def search(self, query: MeasureQuery) -> MeasureSeries:
        ...
