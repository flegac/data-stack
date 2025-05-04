import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from pathlib import Path

import xarray as xr

from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle


@dataclass
class DataFile:
    data_id: str
    source_hash: str
    source_uri: str
    local_path: Path | None = None
    status: DataFileLifecycle = field(default=DataFileLifecycle.created)
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_file(path: Path, data_id: str | None = None):
        if data_id is None:
            data_id = path.name
        return DataFile(
            data_id=data_id,
            source_hash=compute_hash(path),
            source_uri=str(path),
            local_path=path,
        )

    @cached_property
    def raw(self):
        return xr.open_dataset(self.local_path)

    @property
    def variables(self) -> list[str]:
        return list(self.raw.data_vars)

    def __repr__(self):
        return (
            f"data_id: {self.data_id}\n"
            f"status: {self.status.name}\n"
            f"source_uri: {self.source_uri}\n"
            f"local_path: {self.local_path}\n"
            f"source_hash: {self.source_hash}\n"
            f"last_update_date: {self.last_update_date}"
        )


def compute_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
