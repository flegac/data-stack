from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from meteo_domain.sensor.entities.location import Location

type UID = str


class Repository[Entity](ABC):
    @abstractmethod
    async def create_or_update(self, item: Entity) -> UID: ...

    @abstractmethod
    async def insert_batch(self, items: list[Entity]) -> list[Entity]: ...
    @abstractmethod
    async def delete_by_id(self, primary_key: UID): ...
    @abstractmethod
    async def find_by_id(self, primary_key: UID) -> Entity | None: ...
    @abstractmethod
    def find_all(self, **query: Any) -> AsyncGenerator[Entity, Any]: ...
    @abstractmethod
    async def init(self, reset: bool = False): ...


class GeoRepository[Entity](Repository[Entity], ABC):
    @abstractmethod
    async def find_in_radius(
        self, center: Location, radius_km: float
    ) -> list[Entity]: ...


class TimeRepository[Entity](Repository[Entity], ABC):
    @abstractmethod
    async def find_in_period(self, start: str, end: str) -> list[Entity]: ...
