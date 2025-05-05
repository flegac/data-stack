from contextlib import asynccontextmanager

import databases
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class CancelTransactionError(Exception):
    pass


class PgConnection:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = databases.Database(database_url)
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self._current_session = None

    @asynccontextmanager
    async def transaction(self):
        if self._current_session is not None:
            logger.trace("transaction: CONTINUE")
            yield self._current_session
            return

        logger.trace("transaction: START")
        await self.connect()
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
                await self.disconnect()
                logger.trace("transaction: STOP")

    def cancel_transaction(self):
        raise CancelTransactionError

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()
