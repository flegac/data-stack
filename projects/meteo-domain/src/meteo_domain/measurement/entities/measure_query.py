from dataclasses import dataclass

from meteo_domain.measurement.entities.sensor.sensor import Sensor
from meteo_domain.measurement.entities.period import Period


@dataclass(frozen=True)
class MeasureQuery:
    sources: list[Sensor]
    period: Period | None = None
    tags: dict[str, list[str]] | None = None
