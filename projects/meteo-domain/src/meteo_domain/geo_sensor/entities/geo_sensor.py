from dataclasses import dataclass

from meteo_domain.geo_sensor.entities.location.location import Location

type SensorId = str


@dataclass(frozen=True, kw_only=True)
class GeoSensor:
    workspace_id: str | None = None
    uid: SensorId | None = None
    measure_type: str | None = None
    location: Location | None = None

    def __repr__(self):
        return f"{self.uid}[{self.measure_type}]@{self.location}"
