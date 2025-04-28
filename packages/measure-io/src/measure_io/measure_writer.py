from abc import ABC, abstractmethod

from measure_io.measure import MeasureSeries, Measure


class MeasureWriter(ABC):
    @abstractmethod
    def write(self, measure: Measure):
        ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        ...
