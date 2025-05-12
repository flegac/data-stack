from abc import ABC

from aa_common.repo.repository import GeoRepository

from meteo_domain.sensor.entities.sensor import Sensor


class SensorRepository(GeoRepository[Sensor], ABC): ...
