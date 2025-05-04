from contextlib import asynccontextmanager
from datetime import datetime
from typing import override

import databases
from loguru import logger
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from data_file_repository_pg.data_file_model import DataFileModel
from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.ports.data_file_repository import DataFileRepository


class CancelTransactionError(Exception):
    pass


class PgDataFileRepository(DataFileRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.model = DataFileModel

        self._current_session = None

    @asynccontextmanager
    async def transaction(self):
        if self._current_session is not None:
            logger.trace("transaction: CONTINUE")
            yield self._current_session
            return

        logger.trace("transaction: START")
        await self.init()
        async with self.async_session() as session:
            self._current_session = session
            try:
                yield session
                logger.trace("transaction: commit")
                await session.commit()
            except CancelTransactionError:
                logger.trace("transaction: rollback (canceled)")
                await session.rollback()
            except Exception:
                logger.trace("transaction: rollback (error)")
                await session.rollback()
                raise
            finally:
                self._current_session = None
                await self.close()
                logger.trace("transaction: STOP")

    def cancel_transaction(self):
        raise CancelTransactionError

    @override
    async def find_by_id(self, data_id: str):
        async with self.transaction() as session:
            stmt = select(self.model).where(self.model.data_id == data_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                return DataFile(
                    data_id=row.data_id,
                    source_uri=row.source_uri,
                    source_hash=row.source_hash,
                    status=row.status,
                    creation_date=row.creation_date,
                    last_update_date=row.last_update_date,
                )
            return None

    @override
    async def find_by_hash(self, source_hash: str) -> list[DataFile]:
        async with self.transaction() as session:
            stmt = select(self.model).where(self.model.source_hash == source_hash)
            result = await session.execute(stmt)
            return [
                DataFile(
                    data_id=row.data_id,
                    source_uri=row.source_uri,
                    source_hash=row.source_hash,
                    status=row.status,
                    creation_date=row.creation_date,
                    last_update_date=row.last_update_date,
                )
                for row in result.scalars().all()
            ]

    @override
    async def update_status(self, item: DataFile, status: DataFileLifecycle):
        logger.info(f"{item.data_id}: {item.status.name} -> {status.name}")
        async with self.transaction() as session:
            stmt = (
                update(self.model)
                .where(self.model.data_id == item.data_id)
                .values(status=status, last_update_date=datetime.now())
            )
            result = await session.execute(stmt)

        if result.rowcount == 0:
            raise ValueError(f"No DataFile found with uid: {item.data_id}")
        item.status = status

    @override
    async def create_or_update(self, item: DataFile):
        logger.info(f"{item}")
        async with self.transaction() as session:
            item.last_update_date = datetime.now()
            await session.merge(
                self.model(
                    data_id=item.data_id,
                    source_uri=item.source_uri,
                    source_hash=item.source_hash,
                    status=item.status,
                    creation_date=item.creation_date,
                    last_update_date=item.last_update_date,
                )
            )

    @override
    async def delete_by_id(self, data_id: str):
        logger.info(f"{data_id}")
        async with self.transaction() as session:
            await session.execute(
                delete(self.model).where(self.model.data_id == data_id)
            )

    @override
    async def read_all(self):
        async with self.transaction() as session:
            result = await session.execute(select(self.model))
        for row in result.scalars().all():
            yield DataFile(
                data_id=row.data_id,
                source_uri=row.source_uri,
                source_hash=row.source_hash,
                status=row.status,
                creation_date=row.creation_date,
                last_update_date=row.last_update_date,
            )

    @override
    async def init(self):
        await self.database.connect()
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model.metadata.create_all)

    @override
    async def close(self):
        await self.database.disconnect()
