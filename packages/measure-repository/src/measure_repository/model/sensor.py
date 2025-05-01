from dataclasses import dataclass

from measure_repository.model.location import Location
from measure_repository.model.measure_type import MeasureType

type SensorId = str


@dataclass
class Sensor:
    id: SensorId
    type: MeasureType
    location: Location | None = None
