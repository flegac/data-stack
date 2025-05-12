from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any, override

from aa_common.logger import logger
from aa_common.repo.repository import UID, Repository
from sqlalchemy import delete
from sqlmodel import select

from sql_connector.model_mapping import ModelDomainMapper
from sql_connector.sql_connection import SqlConnection


class SqlRepository[Domain, Model](Repository[Domain]):
    def __init__(
        self,
        connection: SqlConnection,
        mapper: ModelDomainMapper[Domain, Model],
    ):
        self.connection = connection
        self.mapper = mapper

    @override
    async def create_or_update(self, item: Domain) -> UID:
        logger.info(f"{item}")
        async with self.connection.transaction() as session:
            item.last_update_date = datetime.now()
            await session.merge(
                self.mapper.to_model(item),
            )
            return getattr(item, self.mapper.primary_key())

    @override
    async def insert_batch(self, items: list[Domain]):
        logger.info(f"{self.__class__.__name__}: {len(items)}")
        now = datetime.now()
        models = []
        for item in items:
            item.last_update_date = now
            models.append(self.mapper.to_model(item))

        async with self.connection.transaction() as session:
            await session.run_sync(
                lambda sync_session: sync_session.bulk_save_objects(models)
            )
        return items

    @override
    async def delete_by_id(self, primary_key: UID):
        logger.info(f"{primary_key}")
        async with self.connection.transaction() as session:
            await session.execute(
                delete(self.mapper.model).where(
                    self.mapper.primary_key() == primary_key
                )
            )

    @override
    async def find_by_id(self, primary_key: UID):
        async with self.connection.transaction() as session:
            stmt = select(self.mapper.model).where(
                self.mapper.primary_key == primary_key
            )
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                return self.mapper.to_domain(row)
            return None

    @override
    async def find_all(self, **query: Any) -> AsyncGenerator[Domain, Any]:
        model = self.mapper.model
        statement = select(model)
        for key, value in query.items():
            statement.where(getattr(self.mapper.model, key) == value)

        async with self.connection.transaction() as session:
            result = await session.execute(statement)
        for row in result.scalars().all():
            yield self.mapper.to_domain(row)

    @override
    async def init(self, reset: bool = False):
        await self.connection.init_table(self.mapper.model, reset)

    @override
    async def close(self):
        await self.connection.disconnect()
