from contextlib import asynccontextmanager
from datetime import datetime
from typing import override

import databases
from loguru import logger
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from data_file_repository.data_file import DataFile
from data_file_repository.data_file_repository import DataFileRepository
from data_file_repository.task_status import TaskStatus
from data_file_repository_pg.data_file_model import DataFileModel


class CancelTransactionException(Exception):
    pass


class PgDataFileRepository(DataFileRepository):

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        self.model = DataFileModel

        self._current_session = None

    @asynccontextmanager
    async def transaction(self):
        if self._current_session is not None:
            logger.trace(f'transaction: CONTINUE')
            yield self._current_session
            return

        logger.trace(f'transaction: START')
        await self.init()
        async with self.async_session() as session:
            self._current_session = session
            try:
                yield session
                logger.trace(f'transaction: commit')
                await session.commit()
            except CancelTransactionException:
                logger.trace(f'transaction: rollback (canceled)')
                await session.rollback()
            except Exception:
                logger.trace(f'transaction: rollback (error)')
                await session.rollback()
                raise
            finally:
                self._current_session = None
                await self.close()
                logger.trace(f'transaction: STOP')

    def cancel_transaction(self):
        raise CancelTransactionException

    @override
    async def find_by_key(self, key: str):
        logger.debug(f'find_by_key: {key}')
        async with self.transaction() as session:
            stmt = select(self.model).where(self.model.key == key)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                return DataFile(
                    key=row.key,
                    source_uri=row.source_uri,
                    source_hash=row.source_hash,
                    status=row.status,
                    creation_date=row.creation_date,
                    last_update_date=row.last_update_date,
                )
            return None

    @override
    async def update_status(self, item: DataFile, status: TaskStatus) -> DataFile:
        logger.debug(f'update_status: {item.key}: {item.status.name} -> {status.name}')
        async with self.transaction() as session:
            stmt = (
                update(self.model)
                .where(self.model.key == item.key)
                .values(status=status, last_update_date=datetime.now())
            )
            result = await session.execute(stmt)

        if result.rowcount == 0:
            raise ValueError(f"No DataFile found with uid: {item.key}")
        return await self.find_by_key(item.key)

    @override
    async def create_or_update(self, item: DataFile):
        logger.debug(f'create_or_update: {item}')
        async with self.transaction() as session:
            item.last_update_date = datetime.now()
            await session.merge(self.model(
                key=item.key,
                source_uri=item.source_uri,
                source_hash=item.source_hash,
                status=item.status,
                creation_date=item.creation_date,
                last_update_date=item.last_update_date,
            ))

    @override
    async def delete_by_key(self, key: str):
        logger.debug(f'delete_by_key: {key}')
        async with self.transaction() as session:
            await session.execute(delete(self.model).where(self.model.key == key))

    @override
    async def read_all(self):
        logger.debug(f'read_all')
        async with self.transaction() as session:
            result = await session.execute(select(self.model))
        for row in result.scalars().all():
            yield DataFile(
                key=row.key,
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
