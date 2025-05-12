from abc import ABC

from aa_common.repo.repository import Repository

from meteo_domain.data_file.entities.datafile import DataFile


class DataFileRepository(Repository[DataFile], ABC): ...
