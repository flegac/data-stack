import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from meteo_domain.data_file.entities.datafile_lifecycle import DataFileLifecycle


@dataclass(kw_only=True)
class DataFile:
    uid: str
    workspace_id: str | None = None
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
        )

    def __repr__(self):
        return (
            f"uid: {self.uid}\n"
            f'workspace_id: "{self.workspace_id}"\n'
            f"status: {self.status.name}\n"
            f"local_path: {self.local_path}\n"
            f"source_hash: {self.source_hash}\n"
        )


def compute_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
