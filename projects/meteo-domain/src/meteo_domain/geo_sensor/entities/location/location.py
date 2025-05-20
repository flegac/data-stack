import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    longitude: float
    latitude: float
    altitude: float = 0.0
    name: str | None = None

    @staticmethod
    def from_raw(raw: tuple[float, float]):
        return Location(
            longitude=raw[0],
            latitude=raw[1],
        )

    @property
    def latitude_rad(self):
        return math.radians(self.latitude)

    @property
    def longitude_rad(self):
        return math.radians(self.longitude)

    @property
    def raw(self):
        return self.longitude, self.latitude

    def __repr__(self):
        return (
            f"[lat={self.latitude:.3f}°N,"
            f" lon={self.longitude:.3f}°E,"
            f" alt={self.altitude:.1f}m]"
        )
