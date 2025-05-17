import asyncio
from unittest import TestCase

from meteo_domain.core.impl.repository_checker import check_uow_repository
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.data_file import SqlDataFileRepository
from sql_meteo_adapters.sensor import (
    SqlSensorRepository,
)
from sql_meteo_adapters.workspace import SqlWorkspaceRepository


class TestRepositories(TestCase):
    def setUp(self):
        # logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.uow = SqlUnitOfWork(
            database_url="postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )

    def test_sensor(self):
        asyncio.run(
            check_uow_repository(
                self.uow,
                SqlSensorRepository(self.uow),
                Sensor(
                    uid="sensor_uid",
                    measure_type="test-type",
                    location=Location(
                        latitude=33.0,
                        longitude=22.0,
                    ),
                ),
            )
        )

    def test_workspace(self):
        asyncio.run(
            check_uow_repository(
                self.uow,
                SqlWorkspaceRepository(self.uow),
                Workspace(uid="ws_id"),
            )
        )

    def test_datafile(self):
        asyncio.run(
            check_uow_repository(
                self.uow,
                SqlDataFileRepository(self.uow),
                DataFile(uid="toto", source_hash="toto-hash"),
            )
        )
