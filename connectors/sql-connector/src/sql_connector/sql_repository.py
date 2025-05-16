from collections.abc import AsyncGenerator
from typing import Any, override

from sqlalchemy import delete
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from meteo_domain.core.logger import logger
from meteo_domain.core.repository import UID, Repository
from sql_connector.model_mapping import ModelDomainMapper


class SqlRepository[Domain, Model](Repository[Domain]):
    def __init__(
        self,
        session: AsyncSession,
        mapper: ModelDomainMapper[Domain, Model],
    ):
        self.session = session
        self.mapper = mapper

    @override
    async def save(self, batch: Domain | list[Domain]):
        items: list[Domain] = batch
        if not isinstance(batch, list):
            logger.info(f"{batch}")
            await self.session.merge(
                self.mapper.to_model(batch),
            )
            return

        logger.info(f"{self.__class__.__name__}: {len(items)}")
        models = []
        for item in items:
            models.append(self.mapper.to_model(item).__dict__)
        # self.session.execute(update(self.mapper.model))

        table = self.mapper.model
        await self.session.run_sync(
            lambda sync_session: sync_session.bulk_update_mappings(table, models)
        )
        # await self.session.run_sync(
        #     lambda sync_session: sync_session.bulk_save_objects(models)
        # )

    @override
    async def delete_by_id(self, primary_key: UID):
        logger.info(f"{primary_key}")
        await self.session.execute(
            delete(self.mapper.model).where(self.mapper.primary_key() == primary_key)
        )

    @override
    async def find_by_id(self, primary_key: UID):

        stmt = select(self.mapper.model).where(self.mapper.primary_key == primary_key)
        result = await self.session.execute(stmt)
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

        result = await self.session.execute(statement)
        for row in result.scalars().all():
            yield self.mapper.to_domain(row)
