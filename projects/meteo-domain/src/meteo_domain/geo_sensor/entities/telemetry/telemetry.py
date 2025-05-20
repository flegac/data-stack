from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Telemetry:
    time: datetime
    value: float

    def __repr__(self):
        return f"[value={self.value}, time={self.time}]"
