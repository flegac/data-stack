from dataclasses import dataclass

from meteo_measures.entities.measures.location import Location
from meteo_measures.entities.measures.measure_type import MeasureType

type SensorId = str


@dataclass
class Sensor:
    id: SensorId
    type: MeasureType
    location: Location | None = None
