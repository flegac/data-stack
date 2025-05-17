from abc import ABC, abstractmethod

from meteo_domain.measurement.entities.sensor.location import Location


class LocationAPI(ABC):
    @abstractmethod
    def haversine_distance(self, loc1: Location, loc2: Location) -> float: ...

    @abstractmethod
    def random_in_radius(self, center: Location, radius_km: float) -> Location: ...
