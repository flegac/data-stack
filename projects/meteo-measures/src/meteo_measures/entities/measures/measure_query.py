from dataclasses import dataclass

from meteo_measures.entities.measures.location import Location
from meteo_measures.entities.measures.measure_type import MeasureType
from meteo_measures.entities.measures.period import Period


@dataclass
class MeasureQuery:
    sensor_id: str | None = None
    period: Period | None = None
    location: Location | None = None
    measure_type: MeasureType | None = None
