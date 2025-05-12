from dataclasses import dataclass

from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.temporal_series.entities.period import Period


@dataclass(frozen=True)
class MeasureQuery:
    sources: list[Sensor]
    period: Period | None = None
    tags: dict[str, list[str]] | None = None
