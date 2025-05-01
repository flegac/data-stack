from typing import override

from measure_repository.model.measure import Measure
from measure_repository.model.measure_series import MeasureSeries
from measure_repository.stream.measure_writer import MeasureWriter


class FileMeasureWriter(MeasureWriter):
    @override
    def write(self, measure: Measure):
        raise NotImplementedError

    @override
    def write_batch(self, measures: MeasureSeries):
        raise NotImplementedError
