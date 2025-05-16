import asyncio
import logging
from dataclasses import dataclass
from unittest import TestCase

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

from meteo_domain.core.impl.repository_checker import check_repository
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


@dataclass
class DomainEntity:
    id: str
    name: str


Base = declarative_base()


class ModelEntity(Base):
    __tablename__ = "modelentity"
    id = Column(String, primary_key=True)
    name: str = Column(String)


class TestSqlRepository(TestCase):
    def setUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)

    def test_transaction(self):
        asyncio.run(self.run_transaction())

    async def run_transaction(self):
        uow = SqlUnitOfWork(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
        mapper = ModelMapper(DomainEntity, ModelEntity)
        repo = SqlRepository(uow, mapper=mapper)

        async with uow.transaction():
            await check_repository(repo, DomainEntity(id="toto", name="toto"))
            print("whatever1")

        async with uow.transaction():
            print("whatever2")
            uow.cancel()
