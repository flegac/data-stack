from abc import abstractmethod, ABC

from data_file_repository.data_file import DataFile
from data_file_repository.task_status import TaskStatus


class DataFileRepository(ABC):

    @abstractmethod
    async def update_status(self, item: DataFile, status: TaskStatus) -> DataFile:
        ...

    @abstractmethod
    async def create_or_update(self, item: DataFile):
        ...

    @abstractmethod
    def find_by_key(self, key: str) -> DataFile | None:
        ...

    @abstractmethod
    async def delete_by_key(self, item: DataFile):
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
