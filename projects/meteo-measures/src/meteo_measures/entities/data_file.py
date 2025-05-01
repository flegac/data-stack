import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from pathlib import Path

import xarray as xr

from meteo_measures.entities.task_status import TaskStatus


@dataclass
class DataFile:
    key: str
    source_hash: str
    source_uri: str
    local_path: Path | None = None
    status: TaskStatus = field(default=TaskStatus.created)
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_file(path: Path, key: str | None = None):
        if key is None:
            key = path.name
        return DataFile(
            key=key,
            source_hash=compute_hash(path),
            source_uri=str(path),
            local_path=path
        )

    @cached_property
    def raw(self):
        return xr.open_dataset(self.local_path)

    @property
    def variables(self) -> list[str]:
        return list(self.raw.data_vars)

    def __repr__(self):
        return f'Data({self.key}, {self.status}, {self.source_hash})'


def compute_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
