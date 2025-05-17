from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from meteo_domain.core.unit_of_work import UnitOfWork
from sql_connector.sql_connection import SqlConnection


class SqlUnitOfWork(UnitOfWork):
    def __init__(self, database_url: str):
        self.connection = SqlConnection(database_url)
        self.session: AsyncSession | None = None

    @override
    async def create_session(self):
        if self.session:
            raise ValueError("Session already exists")
        self.session = self.connection.session_factory()

    @override
    async def destroy_session(self):
        await self.session.close()
        self.session = None

    @override
    async def commit(self):
        await self.session.commit()

    @override
    async def rollback(self):
        await self.session.rollback()
