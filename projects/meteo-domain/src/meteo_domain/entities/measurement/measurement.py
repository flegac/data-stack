from dataclasses import dataclass
from datetime import datetime

from meteo_domain.entities.sensor import Sensor


@dataclass
class Measurement:
    time: datetime
    value: float
    sensor: Sensor | None = None

    def __repr__(self):
        return f"[value={self.value}, time={self.time}]"


@dataclass
class Measurements:
    sensor: Sensor
    measures: list[Measurement]

    @staticmethod
    def from_measures(sensor: Sensor, measures: list[Measurement]):
        return Measurements(
            sensor=sensor,
            measures=measures,
        )

    def __iter__(self):
        for _ in self.measures:
            _.sensor = self.sensor
            yield _

    def __repr__(self):
        return f"{self.sensor}\n{'\n'.join([f'{_.time} {_.value}' for _ in self.measures[:5]])}"
