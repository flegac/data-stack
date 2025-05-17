import asyncio
from unittest import TestCase

from meteo_domain.core.impl.repository_checker import check_uow_repository
from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor
from unit_of_work_sql.sql_unit_of_work import SqlUnitOfWork


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
                self.uow.sensors(),
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
                self.uow.workspaces(),
                Workspace(uid="ws_id"),
            )
        )

    def test_datafile(self):
        asyncio.run(
            check_uow_repository(
                self.uow,
                self.uow.datafiles(),
                DataFile(uid="toto", source_hash="toto-hash"),
            )
        )
