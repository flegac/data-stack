from typing import override

from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.ports.measure_writer import MeasureWriter


class FileMeasureWriter(MeasureWriter):
    @override
    def write(self, measure: Measurement):
        raise NotImplementedError

    @override
    def write_batch(self, measures: MeasureSeries):
        raise NotImplementedError
