import re
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any


class FileRepository(ABC):
    def __init__(self, local_path: Path | str, bucket: str | None = None):
        local_path = Path(local_path)
        local_path.mkdir(parents=True, exist_ok=True)
        self.local_path = local_path
        self._bucket = _check_bucket(bucket or "default")

    def current_bucket(self) -> str:
        return self._bucket

    def change_bucket(self, bucket: str):
        _check_bucket(bucket)
        self._bucket = bucket

    @abstractmethod
    async def create_bucket(self, bucket: str = None): ...

    @abstractmethod
    async def delete_bucket(self, bucket: str = None): ...

    @abstractmethod
    async def upload_file(self, file_id: str, file_content: bytes | IO): ...

    async def download_file(self, file_id: str, target: Path | None = None):
        if target is None:
            target = self.local_path / file_id
        content = await self.read_content(file_id)
        with target.open("wb") as _:
            _.write(content)
        return target

    @abstractmethod
    async def read_content(self, file_id: str) -> bytes | None: ...

    @abstractmethod
    async def list_buckets(self) -> AsyncGenerator[str, Any]: ...

    @abstractmethod
    async def list_files(self) -> AsyncGenerator[str, Any]: ...


S3_BUCKET_PATTERN = re.compile(r"^[a-zA-Z0-9.\-_]{1,255}$")


def _check_bucket(bucket: str) -> str:
    assert bool(S3_BUCKET_PATTERN.match(bucket)), f"Invalid bucket name: {bucket}"
    return bucket
