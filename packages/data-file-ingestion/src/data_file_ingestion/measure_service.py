from typing import Callable

from measure_io.measure import Measure
from measure_io.measure_reader import MeasureReader
from measure_io.measure_writer import MeasureWriter


class MeasureService:
    def __init__(self, reader: MeasureReader, writer: MeasureWriter):
        self.reader = reader
        self.writer = writer

    def apply_pipeline(self, pipeline: Callable[[Measure], Measure]):
        for measures in self.reader.read_all():
            for measure in measures:
                measure = pipeline(measure)
                self.writer.write(measure)
