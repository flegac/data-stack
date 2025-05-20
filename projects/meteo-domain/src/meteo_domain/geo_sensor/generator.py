from dataclasses import dataclass

from meteo_domain.geo_sensor.entities.radial_geo_distribution import (
    RadialGeoDistribution,
)
from meteo_domain.geo_sensor.entities.radial_value_distribution import (
    RadialValueDistribution,
)


@dataclass
class Generator:
    geo: RadialGeoDistribution
    value: RadialValueDistribution

    @property
    def center(self):
        return self.value.center
