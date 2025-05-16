from abc import ABC

from meteo_domain.core.impl.memory_repository import MemRepository
from meteo_domain.core.repository import Repository
from meteo_domain.data_file.entities.datafile import DataFile


class DataFileRepository(Repository[DataFile], ABC): ...


class MemDataFileRepository(DataFileRepository, MemRepository[DataFile]):
    def __init__(self):
        super().__init__(DataFile)
