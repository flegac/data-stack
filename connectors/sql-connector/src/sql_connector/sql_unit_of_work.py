from typing import override

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from meteo_domain.core.unit_of_work import UnitOfWork


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

    async def _init_table(self, model, reset: bool = False):
        await self.database.connect()
        async with self.engine.begin() as conn:
            if reset:
                await conn.run_sync(model.metadata.drop_all)
            await conn.run_sync(model.metadata.create_all)
