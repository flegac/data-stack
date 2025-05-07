from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from meteo_domain.entities.workspace import Workspace


class WorkspaceRepository(ABC):
    @abstractmethod
    async def create_or_update(self, item: Workspace): ...

    @abstractmethod
    async def delete_by_id(self, workspace_id: str): ...

    @abstractmethod
    async def find_by_id(self, workspace_id: str) -> Workspace | None: ...

    @abstractmethod
    async def find_all(self) -> AsyncGenerator[Workspace, None]: ...

    @abstractmethod
    async def init(self): ...

    @abstractmethod
    async def close(self): ...
