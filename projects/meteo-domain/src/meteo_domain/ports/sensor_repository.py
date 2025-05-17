from abc import ABC

from meteo_domain.core.geo_repository import GeoRepository
from meteo_domain.core.repository import Repository
from meteo_domain.sensor.entities.sensor import Sensor


class SensorRepository(Repository[Sensor], GeoRepository[Sensor], ABC):
    pass
