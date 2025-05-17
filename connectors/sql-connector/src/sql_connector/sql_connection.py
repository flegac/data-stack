import re

from sqlalchemy import text, Executable
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from meteo_domain.core.logger import logger


class BaseModel(DeclarativeBase):
    pass


class SqlConnection:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database_name = get_database_name_from_url(self.database_url)

        self.engine = create_async_engine(database_url, echo=False)
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        self.session: AsyncSession | None = None

    async def create_session(self):
        if self.session:
            raise ValueError("Session already exists")
        self.session = self.session_factory()

    async def close_session(self):
        if not self.session:
            raise ValueError("Session does not exist. Call create_session() first.")
        await self.session.close()
        self.session = None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def execute(self, session: AsyncSession, statement: Executable):
        await session.execute(statement)

    async def kill_all_connections(self):
        logger.info("killing all connections")

        # async with asyncio.timeout(5):
        async with self.engine.begin() as conn:
            await conn.execute(
                text(
                    f"""
                     SELECT pg_terminate_backend(pg_stat_activity.pid)
                     FROM pg_stat_activity
                     WHERE pg_stat_activity.datname = '{self.database_name}'
                     AND pid <> pg_backend_pid();
                 """
                )
            )
        logger.info("connections killed")

    async def create_table(self, model: BaseModel):
        async with self.engine.begin() as conn:
            await conn.run_sync(model.metadata.create_all, checkfirst=True)

    async def drop_table(self, model: BaseModel):
        async with self.engine.begin() as conn:
            await conn.run_sync(model.metadata.drop_all, checkfirst=True)


def get_database_name_from_url(database_url: str):
    match = re.search(r"/([^/]+)$", database_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Nom de la base de données non trouvé dans l'URL")
