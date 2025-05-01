from dataclasses import dataclass

from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.period import Period


@dataclass
class MeasureQuery:
    sensor_id: str | None = None
    period: Period | None = None
    location: Location | None = None
    measure_type: str | None = None
    tags: dict[str, list[str]] | None = None
