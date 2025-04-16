from typing import Callable

from measure_feature import MeasureQuery, Measure
from measure_feature.api.measure_reader import MeasureReader
from measure_feature.api.measure_writer import MeasureWriter


class MeasureService:
    def __init__(self, reader: MeasureReader, writer: MeasureWriter):
        self.reader = reader
        self.writer = writer

    def apply_pipeline(
            self,
            query: MeasureQuery,
            pipeline: Callable[[Measure], Measure]
    ):
        measures = self.reader.search(query)

        for measure in measures:
            measure = pipeline(measure)
            self.writer.write(measure)
