import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from data_file_repository.task_status import TaskStatus


@dataclass
class DataFile:
    name: str
    file_uid: str
    status: TaskStatus
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_file(path: Path):
        file_hash = calculate_file_hash(path)
        return DataFile(
            name=path.name,
            file_uid=file_hash,
            status=TaskStatus.created
        )


def calculate_file_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
