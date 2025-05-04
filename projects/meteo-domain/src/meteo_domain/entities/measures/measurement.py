from dataclasses import dataclass
from datetime import datetime

from meteo_domain.entities.measures.sensor import Sensor


@dataclass
class Measurement:
    datetime: datetime
    value: float
    sensor: Sensor | None = None

    def __repr__(self):
        return f"{self.sensor.type}[value={self.value}, time={self.datetime}]"
