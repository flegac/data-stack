from dataclasses import dataclass
from datetime import datetime

from meteo_domain.sensor.entities.sensor import Sensor


@dataclass(frozen=True)
class Measurement:
    time: datetime
    value: float

    def tag(self, sensor: Sensor):
        return TaggedMeasurement(self.time, self.value, sensor)

    def __repr__(self):
        return f"[value={self.value}, time={self.time}]"


@dataclass(frozen=True)
class TaggedMeasurement:
    time: datetime
    value: float
    sensor: Sensor

    def untag(self):
        return Measurement(self.time, self.value)

    def __repr__(self):
        return f"{self.sensor}[value={self.value}, time={self.time}]"
