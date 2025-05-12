from dataclasses import dataclass

from meteo_domain.sensor.entities.location import Location
from meteo_domain.workspace.entities.workspace import WorkObject

type SensorId = str


@dataclass(kw_only=True)
class Sensor(WorkObject):
    uid: SensorId
    measure_type: str | None = None
    location: Location | None = None

    def __repr__(self):
        return f"{self.uid}[{self.measure_type}]@{self.location}"
