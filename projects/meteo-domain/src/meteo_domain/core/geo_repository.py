from abc import ABC, abstractmethod

from meteo_domain.sensor.entities.location import Location


class GeoRepository[Entity](ABC):
    @abstractmethod
    async def find_in_radius(
        self,
        center: Location,
        radius_km: float,
    ) -> list[Entity]: ...
