from typing import override

from measure_feature import Measure, MeasureSeries
from measure_feature.api.measure_writer import MeasureWriter


class GribMeasureWriter(MeasureWriter):
    @override
    def write(self, measure: Measure):
        raise NotImplementedError

    @override
    def write_batch(self, measures: MeasureSeries):
        raise NotImplementedError
