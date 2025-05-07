import logging
from unittest import IsolatedAsyncioTestCase

from aa_common.repo.repository_checker import check_repository
from meteo_domain.entities.workspace import Workspace
from pg_meteo_adapters.ws_repository import PgWorkspaceRepository


class TestWorkspaceRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PgWorkspaceRepository(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )
        await self.repo.init()

    async def test_it(self):
        await check_repository(
            self.repo,
            Workspace(
                uid="ws_id",
                name="ws_name",
            ),
        )
