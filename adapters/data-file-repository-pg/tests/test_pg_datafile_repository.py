import logging
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from meteo_measures.entities import DataFile
from meteo_measures.entities import TaskStatus

from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository


class TestPgDataFileRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        self.repo = PgDataFileRepository(
            database_url="postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase"
        )

    async def test_transaction(self):
        repo = self.repo

        data_file = DataFile.from_file(
            path=Path(__file__).absolute()
        )
        await repo.create_or_update(data_file)
        await self.log_all()

        async with repo.transaction():
            data_file.key = 'toto'
            await repo.create_or_update(data_file)
            await self.log_all()

            data_file.key = 'titi'
            await repo.create_or_update(data_file)
            await self.log_all()
            repo.cancel_transaction()

        await self.log_all()

    async def test_posix_file_repository(self):
        repo = self.repo

        data_file = DataFile.from_file(
            path=Path(__file__).absolute()
        )

        await repo.create_or_update(data_file)
        await self.log_all()

        await repo.update_status(data_file, TaskStatus.ingestion_success)
        await self.log_all()

        await repo.delete_by_key(data_file.key)
        await self.log_all()

    async def log_all(self):
        async for datafile in self.repo.read_all():
            print(datafile.key, datafile.status)
        print('-------------------')
