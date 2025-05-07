import logging
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

from aa_common.repo.repository_checker import check_repository
from pg_connector.model_mapping import ModelMapping
from pg_connector.pg_repository import PgRepository


@dataclass
class Entity:
    id: str
    name: str


Base = declarative_base()


class EntityModel(Base):
    __tablename__ = "__test_entity__"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class TestPgDataFileRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = PgRepository(
            database_url="postgresql+asyncpg://"
            "admin:adminpassword@localhost:5432/meteo-db",
            mapping=ModelMapping(Entity, EntityModel),
        )
        await self.repo.init()

    async def test_transaction(self):
        connection = self.repo.connection

        async with connection.transaction():
            await check_repository(self.repo, Entity(id="toto", name="toto"))
            print("whatever1")
        async with connection.transaction():
            print("whatever2")
            connection.cancel_transaction()
