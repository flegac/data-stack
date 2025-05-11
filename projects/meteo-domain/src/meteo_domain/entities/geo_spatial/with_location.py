from dataclasses import dataclass

from meteo_domain.entities.geo_spatial.location import Location


@dataclass(kw_only=True)
class WithLocation:
    location: Location | None = None
