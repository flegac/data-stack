import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from data_file_ingestion.task_status import TaskStatus


@dataclass
class DataFile:
    name: str
    uri: str
    file_uid: str
    status: TaskStatus = TaskStatus.pending
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def from_file(path: Path):
        file_hash = calculate_file_hash(path)
        print(file_hash)
        return DataFile(
            name=path.name,
            uri=f's3://my-s3/data-file/{file_hash}{path.suffix}',
            file_uid=file_hash,
        )


def calculate_file_hash(file_path: Path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
