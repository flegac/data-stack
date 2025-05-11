from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Period:
    start: datetime | None = None
    end: datetime | None = None

    @staticmethod
    def from_duration(start: datetime, duration: timedelta):
        return Period(start, start + duration)
