import asyncio
import logging
from dataclasses import dataclass
from unittest import TestCase

from sqlmodel import Field, SQLModel

from meteo_domain.core.impl.repository_checker import check_repository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


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

    def test_transaction(self):
        asyncio.run(self.run_transaction())

    async def run_transaction(self):
        uow = SqlUnitOfWork(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )

        async with uow.transaction():
            repo = SqlRepository(
                uow.session, mapper=ModelMapping(DomainEntity, ModelEntity)
            )
            await check_repository(repo, DomainEntity(id="toto", name="toto"))
            print("whatever1")

        async with uow.transaction():
            repo = SqlRepository(
                uow.session, mapper=ModelMapping(DomainEntity, ModelEntity)
            )
            print("whatever2")
            uow.cancel()
