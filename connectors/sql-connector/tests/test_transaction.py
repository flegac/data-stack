import asyncio
import logging
from dataclasses import dataclass
from unittest import TestCase

from sqlmodel import SQLModel, Field

from aa_common.repo.repository_checker import check_repository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository


@dataclass
class DomainEntity:
    id: str
    name: str


class ModelEntity(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str


class TestSqlRepository(TestCase):
    def setUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = SqlRepository(
            connection=SqlConnection(
                "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
            ),
            mapper=ModelMapping(DomainEntity, ModelEntity),
        )

    def test_transaction(self):
        asyncio.run(self.run_transaction())

    async def run_transaction(self):
        await self.repo.init()
        connection = self.repo.connection

        async with connection.transaction():
            await check_repository(self.repo, DomainEntity(id="toto", name="toto"))
            print("whatever1")
        async with connection.transaction():
            print("whatever2")
            connection.cancel_transaction()
