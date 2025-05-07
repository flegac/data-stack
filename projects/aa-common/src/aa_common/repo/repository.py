from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

type UID = str


class Repository[Entity](ABC):

    @abstractmethod
    async def create_or_update(self, item: Entity) -> UID: ...

    @abstractmethod
    async def delete_by_id(self, primary_key: UID): ...

    @abstractmethod
    async def find_by_id(self, primary_key: UID) -> Entity | None: ...

    @abstractmethod
    def find_all(self, query: Any | None = None) -> AsyncGenerator[Entity, Any]: ...

    @abstractmethod
    async def init(self): ...

    @abstractmethod
    async def close(self): ...
