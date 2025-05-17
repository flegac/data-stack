from typing import Any

from geoalchemy2.shape import from_shape, to_shape
from shapely import Point

from meteo_domain.sensor.entities.location import Location
from sql_connector.patches.patch import MapperPatch, Patch


class LocationDomainPatch(Patch):
    def select(self, name: str, value: Any) -> bool:
        return name == "location"

    def patch(self, value: Any) -> Any:
        point = Point(
            value.longitude,
            value.latitude,
        )
        return from_shape(point, srid=4326)


class LocationModelPatch(Patch):
    def select(self, name: str, value: Any) -> bool:
        return name == "location"

    def patch(self, value: Any) -> Any:
        point = to_shape(value)
        return Location(
            longitude=point.x,
            latitude=point.y,
        )


class LocationPatch(MapperPatch):
    def __init__(self):
        super().__init__(
            domain=LocationDomainPatch(),
            model=LocationModelPatch(),
        )
