from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import xarray as xr


@dataclass
class FileConfig:
    path: Path
    variables: list[str]

    @cached_property
    def raw(self):
        return xr.open_dataset(self.path)
