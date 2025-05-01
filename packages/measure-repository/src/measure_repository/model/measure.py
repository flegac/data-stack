from dataclasses import dataclass
from datetime import datetime

from measure_repository.model.sensor import Sensor


@dataclass
class Measure:
    datetime: datetime
    value: float
    sensor: Sensor | None = None

    def __repr__(self):
        return f'{self.sensor.type.name}[value={self.value}, time={self.datetime}]'
