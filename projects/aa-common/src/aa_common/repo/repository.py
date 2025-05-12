from collections.abc import AsyncGenerator
from typing import Any, Protocol

from meteo_domain.sensor.entities.location import Location

type UID = str


class Repository[Entity](Protocol):
    async def create_or_update(self, item: Entity) -> UID: ...

    async def insert_batch(self, items: list[Entity]) -> list[Entity]: ...

    async def delete_by_id(self, primary_key: UID): ...

    async def find_by_id(self, primary_key: UID) -> Entity | None: ...

    def find_all(self, **query: Any) -> AsyncGenerator[Entity, Any]: ...

    async def init(self, reset: bool = False): ...

    async def close(self): ...


class GeoRepository[Entity](Repository[Entity], Protocol):
    async def find_in_radius(
        self, center: Location, radius_km: float
    ) -> list[Entity]: ...


class TimeRepository[Entity](Repository[Entity], Protocol):
    async def find_in_period(self, start: str, end: str) -> list[Entity]: ...
