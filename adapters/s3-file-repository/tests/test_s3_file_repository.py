import asyncio
import logging
from unittest import TestCase

from aa_common.constants import LOCAL_TEST_PATH
from s3_connector.s3_config import S3Config
from s3_connector.s3_connection import S3Connection
from s3_file_repository.s3_file_repository import S3FileRepository


class TestS3FileRepository(TestCase):
    def setUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        config = S3Config(
            endpoint="http://localhost:9000",
            access_key="admin",
            secret_key="adminpassword",
        )
        self.repo = S3FileRepository(
            connection=S3Connection(config),
            local_path=LOCAL_TEST_PATH,
        )

    def test_s3_file_repository(self):
        asyncio.run(self.run_s3_file_repository())

    async def run_s3_file_repository(self):
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
                print(f"\t{file}: {content[:32]}")
