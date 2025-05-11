from dataclasses import dataclass

from meteo_domain.entities.geo_spatial.location import Location


@dataclass
class LocationArea:
    center: Location
    radius_km: float
