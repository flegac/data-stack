from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float
    altitude: float = 0.0

    def __repr__(self):
        return (
            f"(lat={self.latitude:.3f}°N,"
            f" lon={self.longitude:.3f}°E,"
            f" alt={self.altitude:.1f}m)"
        )
