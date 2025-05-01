from abc import ABC, abstractmethod

from meteo_measures.entities.measures.measure import Measure
from meteo_measures.entities.measures.measure_series import MeasureSeries


class MeasureWriter(ABC):
    @abstractmethod
    def write(self, measure: Measure):
        ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        ...
