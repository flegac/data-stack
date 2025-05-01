from abc import ABC, abstractmethod

from measure_repository.model.measure import Measure
from measure_repository.model.measure_series import MeasureSeries


class MeasureWriter(ABC):
    @abstractmethod
    def write(self, measure: Measure):
        ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        ...
