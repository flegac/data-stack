from typing import override

from measure_repository import Measure

from meteo_measures.entities.measures.measure_series import MeasureSeries
from meteo_measures.ports.measure_writer import MeasureWriter


class FileMeasureWriter(MeasureWriter):
    @override
    def write(self, measure: Measure):
        raise NotImplementedError

    @override
    def write_batch(self, measures: MeasureSeries):
        raise NotImplementedError
