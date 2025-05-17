import asyncio
from dataclasses import dataclass
from unittest import TestCase

from sqlalchemy import Column, String

from meteo_domain.core.impl.repository_checker import check_uow_repository
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_connection import BaseModel
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


@dataclass
class DomainEntity:
    uid: str
    name: str


class ModelEntity(BaseModel):
    __tablename__ = "modelentity"
    uid = Column(String, primary_key=True)
    name: str = Column(String)


class TestSqlRepository(TestCase):
    def setUp(self):
        self.uow = SqlUnitOfWork(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
        self.repo = SqlRepository(
            self.uow, mapper=ModelMapper(DomainEntity, ModelEntity)
        )

    def test_repository(self):
        asyncio.run(self.run_repository())

    async def run_repository(self):

        await check_uow_repository(
            self.uow, self.repo, DomainEntity(uid="toto", name="toto")
        )
        print("whatever1")

        async with self.uow.transaction():
            print("whatever2")
            self.uow.cancel()
