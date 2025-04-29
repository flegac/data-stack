import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from data_file_repository.task_status import TaskStatus


@dataclass
class DataFile:
    key: str
    source_hash: str
    source_uri: str
    status: TaskStatus = field(default=TaskStatus.created)
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_file(key: str, path: Path):
        return DataFile(
            key=key,
            source_hash=compute_hash(path),
            source_uri=str(path)
        )

    def __repr__(self):
        return f'Data({self.key}, {self.status}, {self.source_hash})'


def compute_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
