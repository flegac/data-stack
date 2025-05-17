from dataclasses import dataclass

from meteo_domain.measurement.entities.sensor.location import Location

type SensorId = str


@dataclass(frozen=True)
class Sensor:
    uid: SensorId | None = None
    workspace_id: str | None = None
    measure_type: str | None = None
    location: Location | None = None

    def __repr__(self):
        return f"{self.uid}[{self.measure_type}]@{self.location}"
