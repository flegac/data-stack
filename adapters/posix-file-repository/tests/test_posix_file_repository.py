import asyncio
import logging
from unittest import TestCase

from meteo_domain.config import LOCAL_TEST_PATH
from posix_file_repository.posix_file_repository import PosixFileRepository


class TestPosixFileRepository(TestCase):
    def setUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PosixFileRepository(
            remote_path=LOCAL_TEST_PATH / "remote",
            local_path=LOCAL_TEST_PATH / "local",
        )

    def test_posix_file_repository(self):
        asyncio.run(self.posix_file_repository())

    async def posix_file_repository(self):
        repo = self.repo
        key = "toto.txt"
        expected = b"content of file"

        await repo.create_bucket()
        repo.change_bucket("new-bucket")
        await repo.create_bucket()

        await repo.upload_file(key, expected)
        actual = await repo.read_content(key)
        self.assertEqual(expected, actual)

        await repo.download_file(key)

        async for bucket in repo.list_buckets():
            repo.change_bucket(bucket)
            files = [_ async for _ in repo.list_files()]
            print(f"{bucket}: {files}")
            for file in files:
                content = await repo.read_content(file)
                print(f"\t{file}: {content}")
