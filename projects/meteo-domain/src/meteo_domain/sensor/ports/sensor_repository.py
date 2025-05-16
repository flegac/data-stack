from abc import ABC

from meteo_domain.core.repository import GeoRepository
from meteo_domain.sensor.entities.sensor import Sensor


class SensorRepository(GeoRepository[Sensor], ABC): ...
