from typing import override

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from meteo_domain.core.unit_of_work import UnitOfWork
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.model_mapping import ModelMapping
from sql_meteo_adapters.data_file_model import DataFileModel
from sql_meteo_adapters.sensor_mapper import SensorMapper
from sql_meteo_adapters.workspace_model import WorkspaceModel


class SqlUnitOfWork(UnitOfWork):

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = create_async_engine(database_url, echo=False)
        self.session_factory = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session: AsyncSession | None = None

    @override
    async def create_session(self):
        self.session = self.session_factory()

    @override
    async def destroy_session(self):
        await self.session.close()

    @override
    async def commit(self):
        await self.session.commit()

    @override
    async def rollback(self):
        await self.session.rollback()

    @override
    async def save[Entity](self, batch: Entity | list[Entity]):
        class_ = batch
        if isinstance(batch, list):
            class_ = batch[0]
        repo = self._repository(class_)
        await self._init_table(repo.mapper.model)
        await repo.save(batch)

    @override
    async def delete[Entity](self, item: Entity):
        raise NotImplementedError

    def _repository[Entity](self, entity: Entity):
        from sql_connector.sql_repository import SqlRepository

        match entity:
            case DataFile():
                return SqlRepository(
                    self.session, ModelMapping(DataFile, DataFileModel)
                )
            case Workspace():
                return SqlRepository(
                    self.session, ModelMapping(Workspace, WorkspaceModel)
                )
            case Sensor():
                return SqlRepository(self.session, SensorMapper())

        raise ValueError(f"Unknown entity type: {entity}")

    async def _init_table(self, model, reset: bool = False):
        await self.database.connect()
        async with self.engine.begin() as conn:
            if reset:
                await conn.run_sync(model.metadata.drop_all)
            await conn.run_sync(model.metadata.create_all)
