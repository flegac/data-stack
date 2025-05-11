import logging
from unittest import IsolatedAsyncioTestCase

from aa_common.repo.repository_checker import check_repository
from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.workspace import Workspace
from sql_connector.sql_connection import SqlConnection
from sql_meteo_adapters.data_file_repository import SqlDataFileRepository
from sql_meteo_adapters.workspace_repository import SqlWorkspaceRepository


class TestRepositories(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.connection = SqlConnection(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )

    async def test_it(self):
        for repo, item in [
            (
                SqlDataFileRepository(self.connection),
                DataFile(uid="toto", source_hash="toto-hash"),
            ),
            (
                SqlWorkspaceRepository(self.connection),
                Workspace(uid="ws_id", name="ws_name"),
            ),
        ]:
            with self.subTest(f"{repo.__class__.__name__}"):
                await repo.init()
                await check_repository(
                    repo,
                    item,
                )
