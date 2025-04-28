from abc import abstractmethod, ABC

from data_file_ingestion.data_file import DataFile


class DataFileRepository(ABC):

    @abstractmethod
    async def create_or_update(self, item: DataFile):
        ...

    @abstractmethod
    async def delete(self, item_uri: str):
        ...

    @abstractmethod
    async def read_all(self):
        ...

    @abstractmethod
    async def init(self):
        ...

    @abstractmethod
    async def close(self):
        ...
