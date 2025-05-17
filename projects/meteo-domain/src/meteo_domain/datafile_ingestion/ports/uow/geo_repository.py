from abc import ABC, abstractmethod

from meteo_domain.datafile_ingestion.ports.uow.repository import Repository
from meteo_domain.measurement.entities.sensor.location import Location


class GeoRepository[Entity](Repository[Entity], ABC):
    @abstractmethod
    async def find_in_radius(
        self,
        center: Location,
        radius_km: float,
    ) -> list[Entity]: ...
