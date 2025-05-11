import logging
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from sqlmodel import SQLModel, Field

from aa_common.repo.repository_checker import check_repository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_repository import SqlRepository


@dataclass
class Entity:
    id: str
    name: str


class EntityModel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str


class TestSqlRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = SqlRepository(
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
