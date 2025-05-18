from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Period:
    start: datetime | None = None
    end: datetime | None = None

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def split(self, n: int):
        delta = self.duration / (n + 1)
        return [self.start + i * delta for i in range(n + 2)]

    @staticmethod
    def from_duration(start: datetime, duration: timedelta):
        return Period(start, start + duration)
