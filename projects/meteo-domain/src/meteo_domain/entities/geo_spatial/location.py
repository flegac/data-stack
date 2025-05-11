from dataclasses import dataclass


@dataclass
class Location:
    latitude: float
    longitude: float
    altitude: float = 0.0

    def __repr__(self):
        return f"(lat={self.latitude:.3f}°N, lon={self.longitude:.3f}°E, alt={self.altitude:.1f}m)"
