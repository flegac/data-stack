from abc import ABC, abstractmethod

from measure_feature import Measure, MeasureSeries


class MeasureWriter(ABC):
    @abstractmethod
    def write(self, measure: Measure):
        ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        ...
