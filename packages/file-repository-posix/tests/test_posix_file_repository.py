import logging
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from file_repository_posix.posix_file_repository import PosixFileRepository


class TestPosixFileRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        self.repo = PosixFileRepository(
            remote_path=Path('/tmp/test/remote'),
            local_path=Path('/tmp/test/local'),
        )

    async def test_posix_file_repository(self):
        repo = self.repo
        key = 'toto.txt'
        expected = 'content of file'.encode('utf-8')

        await repo.create_bucket()
        repo.change_bucket('new-bucket')
        await repo.create_bucket()

        await repo.upload_file(key, expected)
        actual = await repo.read_content(key)
        self.assertEqual(expected, actual)

        await repo.download_file(key)

        async for bucket in repo.list_buckets():
            repo.change_bucket(bucket)
            files = [_ async for _ in repo.list_files()]
            print(f'{bucket}: {files}')
            for file in files:
                content = await repo.read_content(file)
                print(f'\t{file}: {content}')
