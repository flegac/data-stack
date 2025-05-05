from dataclasses import dataclass, field
from functools import cached_property

from meteo_domain.entities.meta_data_file.coordinate import Coordinate
from meteo_domain.entities.meta_data_file.variable import Variable


@dataclass
class MetaDataFile:
    coords: list[Coordinate]
    variables: list[Variable]
    metadata: dict[str, str] = field(default_factory=dict)

    @cached_property
    def coord_sizes(self):
        return {_.name: _.size for _ in self.coords}

    def get_variable_shape(self, variable: Variable):
        return tuple(self.coord_sizes[_] for _ in variable.coords)

    def format_variable_shape(self, variable: Variable):
        shape = self.get_variable_shape(variable)
        return ",".join(
            [
                f"{name}:{size}"
                for name, size in zip(variable.coords, shape, strict=False)
            ]
        )

    def check_coords(self):
        coords = {_.name for _ in self.coords}
        unknown_coords: dict[str, set[str]] = {}
        for var in self.variables:
            var_coords = set(var.coords)
            if not coords.issuperset(var_coords):
                unknown_coords[var.name] = var_coords.difference(coords)
        if unknown_coords:
            raise ValueError(unknown_coords)

    def __repr__(self):
        variables = tuple(
            f"\t- {_.name:15s}: {tuple(_.coords)} {self.get_variable_shape(_)}"
            for _ in self.variables
        )
        return f"{self.metadata}\n{'\n'.join(variables)}"
