from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any, override

from loguru import logger

from meteo_domain.ports.file_repository import FileRepository


class PosixFileRepository(FileRepository):
    def __init__(self, remote_path: Path, local_path: Path, bucket: str | None = None):
        super().__init__(local_path, bucket)
        self.root = remote_path

    @override
    async def create_bucket(self, bucket: str = None):
        if bucket is None:
            bucket = self.current_bucket()
        logger.info(f"{bucket}")
        path = self.root / bucket
        path.mkdir(parents=True, exist_ok=True)

    @override
    async def delete_bucket(self, bucket: str = None):
        path = self.root / bucket
        path.rmdir()

    @override
    async def upload_file(self, file_id: str, file_content: bytes | IO):
        logger.info(f"{file_id}: size={len(file_content) / 1024}Ko")

        path = self.root / self.current_bucket() / file_id
        with path.open("wb") as _:
            _.write(file_content)

    @override
    async def read_content(self, file_id: str) -> bytes | None:
        logger.info(f"{file_id}")

        path = self.root / self.current_bucket() / file_id
        with path.open("rb") as _:
            return _.read()

    @override
    async def list_buckets(self):
        path = self.root
        for _ in path.iterdir():
            if _.is_dir():
                yield _.name

    @override
    async def list_files(self) -> AsyncGenerator[str, Any]:
        path = self.root / self.current_bucket()
        for _ in path.iterdir():
            if _.is_file():
                yield _.name
