import asyncio
from unittest import TestCase

from meteo_domain.core.impl.repository_checker import check_repository
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.models import SensorModel
from sql_meteo_adapters.repositories import (
    SqlWorkspaceRepository,
    SqlDataFileRepository,
    SqlSensorRepository,
)


class TestRepositories(TestCase):
    def setUp(self):
        # logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.uow = SqlUnitOfWork(
            database_url="postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )

    def test_sensor(self):
        repo = SqlSensorRepository(self.uow)
        item = Sensor(
            uid="sensor_uid",
            measure_type="test-type",
            location=Location(
                latitude=33.0,
                longitude=22.0,
            ),
        )
        asyncio.run(self.run_repo_check(repo, item))

    def test_workspace(self):
        repo = SqlWorkspaceRepository(self.uow)
        item = Workspace(uid="ws_id")
        asyncio.run(self.run_repo_check(repo, item))

    def test_datafile(self):
        repo = SqlDataFileRepository(self.uow)
        item = DataFile(uid="toto", source_hash="toto-hash")
        asyncio.run(self.run_repo_check(repo, item))

    async def run_repo_check[Entity](self, repo: SqlRepository, item: Entity):
        await self.uow._init_table(SensorModel)

        async with self.uow.transaction():
            await check_repository(
                repo,
                item,
            )
