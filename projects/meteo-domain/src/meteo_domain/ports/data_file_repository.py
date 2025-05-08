from abc import abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass

from aa_common.repo.repository import Repository
from meteo_domain.entities.data_file import DataFile


@dataclass
class DataFileQuery:
    workspace_id: str | None = None
    source_hash: str | None = None


class DataFileRepository(Repository[DataFile]):

    @abstractmethod
    def find_all(
        self, query: DataFileQuery | None = None
    ) -> AsyncGenerator[DataFile, None]: ...
