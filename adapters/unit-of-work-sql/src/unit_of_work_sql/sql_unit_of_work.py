from typing import override

from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from meteo_domain.datafile_ingestion.ports.uow.geo_repository import (
    GeoRepository,
)
from meteo_domain.datafile_ingestion.ports.uow.repository import Repository
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork
from meteo_domain.measurement.entities.sensor.sensor import Sensor
from sql_connector.sql_connection import SqlConnection
from unit_of_work_sql.repositories.data_file import SqlDataFileRepository
from unit_of_work_sql.repositories.sensor import SqlSensorRepository
from unit_of_work_sql.repositories.workspace import SqlWorkspaceRepository


class SqlUnitOfWork(UnitOfWork):

    def __init__(self, database_url: str):
        self.connection = SqlConnection(database_url)
        self._sensors = SqlSensorRepository(self.connection)
        self._workspaces = SqlWorkspaceRepository(self.connection)
        self._datafiles = SqlDataFileRepository(self.connection)

    @override
    async def on_start(self):
        await self.connection.create_session()

    @override
    async def on_stop(self):
        await self.connection.close_session()

    @override
    async def commit(self):
        await self.connection.commit()

    @override
    async def rollback(self):
        await self.connection.rollback()

    @override
    def datafiles(self) -> Repository[DataFile]:
        return self._datafiles

    @override
    def workspaces(self) -> Repository[Workspace]:
        return self._workspaces

    @override
    def sensors(self) -> GeoRepository[Sensor]:
        return self._sensors
