import logging
from unittest import IsolatedAsyncioTestCase

from aa_common.repo.repository_checker import check_repository
from meteo_domain.entities.data_file import DataFile
from pg_meteo_adapters.data_file_repository import PgDataFileRepository


class TestDataFileRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PgDataFileRepository(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )
        await self.repo.init()

    async def test_it(self):

        await check_repository(
            self.repo,
            DataFile(uid="toto", source_hash="toto-hash"),
        )
