import asyncio
from unittest import TestCase

from aa_common.repo.repository_checker import check_repository
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository
from sql_meteo_adapters.data_file_repository import SqlDataFileRepository
from sql_meteo_adapters.workspace_repository import SqlWorkspaceRepository


class TestRepositories(TestCase):
    def setUp(self):
        # logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.connection = SqlConnection(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db"
        )

    def test_workspace(self):
        repo = SqlWorkspaceRepository(self.connection)
        item = Workspace(uid="ws_id", name="ws_name")
        asyncio.run(self.run_repo_check(repo, item))

    def test_datafile(self):
        repo = SqlDataFileRepository(self.connection)
        item = DataFile(uid="toto", source_hash="toto-hash")
        asyncio.run(self.run_repo_check(repo, item))

    async def run_repo_check[Entity](self, repo: SqlRepository, item: Entity):
        await repo.init()
        await check_repository(
            repo,
            item,
        )
