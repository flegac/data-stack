from collections.abc import Generator
from typing import Any, override

from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.ports.measure_reader import MeasureReader

from measure_repository_datafile.data_file_measure_repository import (
    DataFileMeasureRepository,
)


class DataFileMeasureReader(MeasureReader):
    def __init__(self, data_file: DataFile):
        super().__init__()
        self.data_file = data_file
        self.delegate = DataFileMeasureRepository(data_file)

    @override
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        return self.delegate.search(None)
