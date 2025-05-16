from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

type UID = str


class Repository[Entity](ABC):
    @abstractmethod
    async def save(
        self,
        batch: Entity | list[Entity],
    ): ...
    @abstractmethod
    async def delete_by_id(
        self,
        primary_key: UID,
    ): ...
    @abstractmethod
    async def find_by_id(
        self,
        primary_key: UID,
    ) -> Entity | None: ...
    @abstractmethod
    def find_all(
        self,
        **query: Any,
    ) -> AsyncGenerator[Entity, Any]: ...
