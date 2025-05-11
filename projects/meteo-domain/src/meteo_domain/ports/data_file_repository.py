from abc import ABC

from aa_common.repo.repository import Repository
from meteo_domain.entities.datafile import DataFile


class DataFileRepository(Repository[DataFile], ABC): ...
