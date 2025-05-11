from dataclasses import dataclass
from datetime import datetime

from meteo_domain.entities.sensor import Sensor


@dataclass
class Measurement:
    time: datetime
    value: float
    sensor: Sensor | None = None

    def __repr__(self):
        return f"{self.sensor.measure_type}[value={self.value}, time={self.time}]"
