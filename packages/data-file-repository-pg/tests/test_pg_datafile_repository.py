import logging
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from data_file_repository.data_file import DataFile
from data_file_repository.task_status import TaskStatus
from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository


class TestPgDataFileRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        self.repo = PgDataFileRepository(
            database_url="postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase"
        )
        await self.repo.init()

    async def asyncTearDown(self):
        await self.repo.close()

    async def test_transaction(self):
        repo = self.repo

        datafile = DataFile.from_file(
            path=Path(__file__).absolute()
        )
        await repo.create_or_update(datafile)
        await self.log_all()

        async with repo.transaction():
            datafile.file_uid = 'toto'
            await repo.create_or_update(datafile)
            await self.log_all()

            datafile.file_uid = 'titi'
            await repo.create_or_update(datafile)
            await self.log_all()
            repo.cancel_transaction()

        await self.log_all()

    async def test_posix_file_repository(self):
        repo = self.repo

        datafile = DataFile.from_file(
            path=Path(__file__).absolute()
        )

        await repo.create_or_update(datafile)
        await self.log_all()

        await repo.update_status(datafile, TaskStatus.ingestion_success)
        await self.log_all()

        await repo.delete(datafile.file_uid)
        await self.log_all()

    async def log_all(self):
        async for datafile in self.repo.read_all():
            print(datafile.file_uid, datafile.status)
        print('-------------------')
