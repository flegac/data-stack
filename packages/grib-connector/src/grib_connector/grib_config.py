from dataclasses import dataclass
from pathlib import Path


@dataclass
class GribConfig:
    path: Path
    variable_name: str
