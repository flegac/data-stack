import logging
from unittest import IsolatedAsyncioTestCase

from meteo_domain.entities.workspace import Workspace
from pg_ws_repository.pg_ws_repository import PgWorkspaceRepository


class TestPgWorkspaceRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PgWorkspaceRepository(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )
        await self.repo.init()

    async def test_it(self):
        repo = self.repo

        item = Workspace(
            workspace_id="ws_id",
            name="ws_name",
        )

        await repo.create_or_update(item)
        await self.log_all()

        await repo.delete_by_id(item.workspace_id)
        await self.log_all()

    async def log_all(self):
        async for item in self.repo.find_all():
            print(item.workspace_id, item.name)
        print("-------------------")
