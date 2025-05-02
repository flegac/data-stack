from abc import ABC, abstractmethod

from meteo_measures.domain.entities.measures.measure_series import MeasureSeries
from meteo_measures.domain.entities.measures.measurement import Measurement


class MeasureWriter(ABC):
    @abstractmethod
    def write(self, measure: Measurement): ...

    @abstractmethod
    def write_batch(self, measures: MeasureSeries): ...
