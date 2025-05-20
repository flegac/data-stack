from dataclasses import dataclass

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.times.period import Period


@dataclass(frozen=True)
class MeasureQuery:
    sources: list[GeoSensor]
    period: Period | None = None
    tags: dict[str, list[str]] | None = None
