import logging
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from pg_datafile_repository.pg_data_file_repository import PgDataFileRepository


class TestPgDataFileRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PgDataFileRepository(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )

    async def test_transaction(self):
        repo = self.repo

        data_file = DataFile.from_file(path=Path(__file__).absolute())
        await repo.create_or_update(data_file)
        await self.log_all()

        async with repo.connection.transaction():
            data_file.data_id = "toto"
            await repo.create_or_update(data_file)
            await self.log_all()

            data_file.data_id = "titi"
            await repo.create_or_update(data_file)
            await self.log_all()
            repo.connection.cancel_transaction()

        await self.log_all()

    async def test_it(self):
        repo = self.repo

        item = DataFile.from_file(path=Path(__file__).absolute())

        await repo.create_or_update(item)
        await self.log_all()

        await repo.update_status(item, DataFileLifecycle.ingestion_completed)
        await self.log_all()

        await repo.delete_by_id(item.data_id)
        await self.log_all()

    async def log_all(self):
        async for datafile in self.repo.find_all():
            print(datafile.data_id, datafile.status)
        print("-------------------")
