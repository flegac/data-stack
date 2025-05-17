from collections.abc import AsyncGenerator
from typing import Any, override

from sqlalchemy import delete, select, Column

from meteo_domain.core.logger import logger
from meteo_domain.core.repository import UID, Repository
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_unit_of_work import SqlUnitOfWork


class SqlRepository[Domain, Model](Repository[Domain]):

    def __init__(
        self,
        uow: SqlUnitOfWork,
        mapper: ModelMapper[Domain, Model],
    ):
        self.uow = uow
        self.mapper = mapper

    @override
    def model_name(self) -> str:
        return self.mapper.domain.__name__

    @override
    async def save(self, batch: Domain | list[Domain]):
        items: list[Domain] = batch
        # if not isinstance(batch, list):
        #     items = [batch]
        if not isinstance(batch, list):
            logger.info(f"{self.model_name()}: {batch}")
            await self.session.merge(
                self.mapper.to_model(batch),
            )
            return

        logger.info(f"{self.model_name()}: {len(items)}")
        models = []
        for item in items:
            models.append(self.mapper.to_model(item).__dict__)
        # self.session.execute(update(self.mapper.model))

        await self.session.run_sync(
            # lambda session: session.bulk_update_mappings(self.model, models)
            lambda session: session.bulk_insert_mappings(self.model, models)
            # lambda session: session.bulk_save_objects(models)
        )

    @override
    async def delete_by_id(self, primary_key: UID):
        logger.info(f"{primary_key}")
        await self.session.execute(
            delete(self.model).where(self.mapper.primary_key_column == primary_key)
        )

    @override
    async def find_by_id(self, primary_key: UID):
        stmt = select(self.model).where(self.mapper.primary_key_column == primary_key)
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            return self.mapper.to_domain(row)
        return None

    @override
    async def find_all(self, **query: Any) -> AsyncGenerator[Domain, Any]:
        statement = select(self.model)
        for key, value in query.items():
            column: Column = getattr(self.model, key)
            statement.where(column == value)

        result = await self.session.execute(statement)
        for row in result.scalars().all():
            yield self.mapper.to_domain(row)

    @override
    async def create_table(self):
        await self.uow.connection.create_table(self.model)

    @override
    async def drop_table(self):
        await self.uow.connection.drop_table(self.model)

    @property
    def session(self):
        return self.uow.session

    @property
    def model(self) -> Model:
        return self.mapper.model
