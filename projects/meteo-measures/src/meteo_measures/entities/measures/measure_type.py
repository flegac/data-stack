from enum import Enum, auto


class MeasureType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()
    PRESSURE = auto()
    WIND_SPEED = auto()
    RAIN = auto()
