from abc import ABC

from aa_common.repo.repository import GeoRepository
from meteo_domain.entities.sensor import Sensor


class SensorRepository(GeoRepository[Sensor], ABC): ...
