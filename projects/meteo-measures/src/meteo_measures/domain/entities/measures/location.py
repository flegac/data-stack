from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float
    altitude: float = 0.0
