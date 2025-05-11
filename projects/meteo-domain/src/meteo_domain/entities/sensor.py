from dataclasses import dataclass

from meteo_domain.entities.geo_spatial.with_location import WithLocation
from meteo_domain.entities.workspace import WorkObject

type SensorId = str


@dataclass(kw_only=True)
class Sensor(WorkObject, WithLocation):
    uid: SensorId
    measure_type: str | None = None

    def __repr__(self):
        return f"{self.uid}[{self.measure_type}]@{self.location}"
