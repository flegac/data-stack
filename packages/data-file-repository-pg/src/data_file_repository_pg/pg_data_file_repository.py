from datetime import datetime
from typing import override

import databases
from sqlalchemy import delete, Column, String, DateTime, Enum as SqlEnum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, declarative_base

from data_file_ingestion.data_file import DataFile
from data_file_ingestion.task_status import TaskStatus
from data_file_ingestion.data_file_repository import DataFileRepository

Base = declarative_base()


class PgDataFileRepository(DataFileRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        self.model = self._create_model()

    def _create_model(self):
        class DataFileModel(Base):
            __tablename__ = 'datafile'
            name = Column(String, nullable=False)
            uri = Column(String, primary_key=True)
            file_uid = Column(String, nullable=False)
            creation_date = Column(DateTime, nullable=False, default=datetime.now)
            last_update_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
            status = Column(SqlEnum(TaskStatus), nullable=False)

        return DataFileModel

    @override
    async def init(self):
        await self.database.connect()
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model.metadata.create_all)

    @override
    async def create_or_update(self, item: DataFile):
        async with self.async_session() as session:
            # Mettre à jour la date de dernière mise à jour
            item.last_update_date = datetime.now()
            await session.merge(self.model(
                name=item.name,
                uri=item.uri,
                file_uid=item.file_uid,
                creation_date=item.creation_date,
                last_update_date=item.last_update_date,
                status=item.status
            ))
            await session.commit()

    @override
    async def delete(self, item_uri: str):
        async with self.async_session() as session:
            await session.execute(delete(self.model).where(self.model.uri == item_uri))
            await session.commit()

    @override
    async def read_all(self):
        async with self.async_session() as session:
            result = await session.execute(select(self.model))
            for row in result.scalars().all():
                yield DataFile(
                    name=row.name,
                    uri=row.uri,
                    file_uid=row.file_uid,
                    creation_date=row.creation_date,
                    last_update_date=row.last_update_date,
                    status=row.status
                )

    @override
    async def close(self):
        await self.database.disconnect()
