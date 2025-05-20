from typing import Any

from geoalchemy2.shape import from_shape, to_shape
from meteo_domain.geo_sensor.entities.location.location import Location
from shapely import Point
from sql_connector.patch import MapperPatch, Patch


class LocationDomainPatch(Patch):
    def select(self, name: str, value: Any) -> bool:
        return name == "location"

    def patch(self, name: str, value: Any):
        point = Point(
            value.longitude,
            value.latitude,
        )
        return name, from_shape(point, srid=4326)


class LocationModelPatch(Patch):
    def select(self, name: str, value: Any) -> bool:
        return name == "location"

    def patch(self, name: str, value: Any):
        point = to_shape(value)
        return name, Location(
            longitude=point.x,
            latitude=point.y,
        )


class LocationPatch(MapperPatch):
    def __init__(self):
        super().__init__(
            domain=LocationDomainPatch(),
            model=LocationModelPatch(),
        )
