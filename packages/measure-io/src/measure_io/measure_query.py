from dataclasses import dataclass
from datetime import datetime

from measure_io.sensor import MeasureType, Location


@dataclass
class Period:
    start: datetime
    end: datetime


@dataclass
class MeasureQuery:
    sensor_id: str | None = None
    period: Period | None = None
    location: Location | None = None
    measure_type: MeasureType | None = None
