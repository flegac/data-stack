from abc import ABC, abstractmethod
from pathlib import Path

from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.meta_data_file import MetaDataFile


class DatafileAPI[RawData](ABC):
    @abstractmethod
    def load_from_datafile(self, item: DataFile) -> MetaDataFile: ...
    @abstractmethod
    def randomize(self, metadata_file: MetaDataFile, output_file: Path) -> DataFile: ...

    @abstractmethod
    def load_raw_data(self, item: DataFile) -> RawData: ...
