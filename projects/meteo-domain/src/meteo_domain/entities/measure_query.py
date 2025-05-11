from dataclasses import dataclass

from meteo_domain.entities.sensor import Sensor
from meteo_domain.entities.temporal.period import Period


@dataclass
class MeasureQuery:
    sources: list[Sensor]
    period: Period | None = None
    tags: dict[str, list[str]] | None = None
