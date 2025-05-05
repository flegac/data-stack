from abc import ABC, abstractmethod

from meteo_domain.entities.workspace.workspace import Workspace


class WorkspaceRepository(ABC):
    @abstractmethod
    async def create(self, workspace: Workspace) -> Workspace: ...

    @abstractmethod
    async def update(self, workspace: Workspace) -> Workspace: ...

    @abstractmethod
    async def delete(self, workspace: Workspace): ...

    @abstractmethod
    async def find_by_id(self, workspace_id: str) -> Workspace | None: ...

    @abstractmethod
    async def find_all(self) -> list[Workspace]: ...
