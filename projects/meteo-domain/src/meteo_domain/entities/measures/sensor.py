from dataclasses import dataclass

from meteo_domain.entities.measures.location import Location

type SensorId = str


@dataclass
class Sensor:
    id: SensorId
    type: str
    location: Location | None = None
