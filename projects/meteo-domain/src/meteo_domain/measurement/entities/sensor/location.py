import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float
    altitude: float = 0.0
    name: str | None = None

    @property
    def latitude_rad(self):
        return math.radians(self.latitude)

    @property
    def longitude_rad(self):
        return math.radians(self.longitude)

    def __repr__(self):
        return (
            f"(lat={self.latitude:.3f}°N,"
            f" lon={self.longitude:.3f}°E,"
            f" alt={self.altitude:.1f}m)"
        )
