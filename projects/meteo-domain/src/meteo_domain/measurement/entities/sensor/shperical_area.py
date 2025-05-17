from dataclasses import dataclass

from meteo_domain.measurement.entities.sensor.location import Location


@dataclass(frozen=True)
class SphericalArea:
    center: Location
    radius_km: float
