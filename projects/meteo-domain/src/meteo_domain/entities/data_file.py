import hashlib
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import xarray as xr

from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.entities.meta_data_file.coordinate import Coordinate
from meteo_domain.entities.meta_data_file.meta_data_file import MetaDataFile
from meteo_domain.entities.meta_data_file.variable import Variable
from meteo_domain.entities.workspace import WorkObject


@dataclass(kw_only=True)
class DataFile(WorkObject):
    uid: str
    source_hash: str
    local_path: Path | None = None
    status: DataFileLifecycle = field(default=DataFileLifecycle.created)

    @staticmethod
    def from_file(path: Path, uid: str | None = None):
        if uid is None:
            uid = path.name
        return DataFile(
            uid=uid,
            source_hash=compute_hash(path),
            local_path=path,
        ).auto_check()

    @cached_property
    def raw(self):
        return xr.open_dataset(self.local_path)

    @cached_property
    def metadata(self):
        raw = self.raw
        return MetaDataFile(
            coords=[Coordinate(str(k), list(v)) for k, v in raw.coords.items()],
            variables=[
                Variable(str(k), list(v.coords.keys()))
                for k, v in raw.data_vars.items()
                if "bounds" not in k
            ],
            metadata=raw.attrs,
        )

    @property
    def variables(self) -> list[str]:
        return list(self.raw.data_vars)

    def auto_check(self):
        self.metadata.check_coords()
        return self

    def __repr__(self):
        return (
            f"uid: {self.uid}\n"
            f'workspace_id: "{self.workspace_id}"\n'
            f'tags: "{self.tags}"\n'
            f"status: {self.status.name}\n"
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
