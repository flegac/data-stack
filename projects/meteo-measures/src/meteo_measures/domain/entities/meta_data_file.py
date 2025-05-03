from dataclasses import dataclass, field
from functools import cached_property

from meteo_measures.domain.entities.coordinate import Coordinate
from meteo_measures.domain.entities.variable import Variable


@dataclass
class MetaDataFile:
    coords: list[Coordinate]
    variables: list[Variable]
    metadata: dict[str, str] = field(default_factory=dict)

    @cached_property
    def coord_sizes(self):
        return {_.name: _.size for _ in self.coords}

    def check_coords(self):
        coords = {_.name for _ in self.coords}
        unknown_coords: dict[str, set[str]] = {}
        for var in self.variables:
            var_coords = set(var.coords)
            if not coords.issuperset(var_coords):
                unknown_coords[var.name] = var_coords.difference(coords)
        if unknown_coords:
            raise ValueError(unknown_coords)
