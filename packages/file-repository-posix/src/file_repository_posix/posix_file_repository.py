from pathlib import Path
from typing import Optional, override, IO

from loguru import logger

from file_repository.file_repository import FileRepository


class PosixFileRepository(FileRepository):
    def __init__(self, remote_path: Path, local_path: Path, bucket: str | None = None):
        super().__init__(local_path, bucket)
        self.root = remote_path

    @override
    async def create_bucket(self):
        logger.debug(f'create_bucket: {self.current_bucket()}')
        path = self.root / self.current_bucket()
        path.mkdir(parents=True, exist_ok=True)

    @override
    async def upload_file(self, key: str, file_content: bytes | IO):
        logger.debug(f'upload_file: {key}: size={len(file_content)/1024}Ko')

        path = self.root / self.current_bucket() / key
        with path.open('wb') as _:
            _.write(file_content)

    @override
    async def read_content(self, key: str) -> Optional[bytes]:
        logger.debug(f'read_content: {key}')

        path = self.root / self.current_bucket() / key
        with path.open('rb') as _:
            return _.read()

    @override
    async def list_buckets(self):
        path = self.root
        for _ in path.iterdir():
            if _.is_dir():
                yield _.name

    @override
    async def list_files(self):
        path = self.root / self.current_bucket()
        for _ in path.iterdir():
            if _.is_file():
                yield _.name
