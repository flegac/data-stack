from dataclasses import dataclass
from datetime import datetime

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.telemetry.telemetry import Telemetry


@dataclass(frozen=True)
class TaggedTelemetry:
    time: datetime
    value: float
    sensor: GeoSensor

    @staticmethod
    def tag(sensor: GeoSensor, telemetry: Telemetry):
        return TaggedTelemetry(
            time=telemetry.time,
            value=telemetry.value,
            sensor=sensor,
        )

    def untag(self):
        return Telemetry(self.time, self.value)

    def __repr__(self):
        return f"{self.sensor}[value={self.value}, time={self.time}]"
