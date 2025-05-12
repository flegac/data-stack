from dataclasses import dataclass

from meteo_domain.sensor.entities.location import Location


@dataclass(frozen=True)
class SphericalArea:
    center: Location
    radius_km: float
