from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Location:
    latitude: float
    longitude: float
    altitude: float = .0


class MeasureType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()
    PRESSURE = auto()
    WIND_SPEED = auto()
    RAIN = auto()


type SensorId = str


@dataclass
class Sensor:
    id: SensorId
    type: MeasureType
    location: Location
