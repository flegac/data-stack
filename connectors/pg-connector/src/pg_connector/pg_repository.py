from datetime import datetime
from typing import override, Any, AsyncGenerator

from sqlalchemy import delete, select

from aa_common.logger import logger
from aa_common.repo.repository import Repository, UID
from pg_connector.model_mapping import ModelMapping
from pg_connector.pg_connection import PgConnection


class PgRepository[Entity, DbModel](Repository[Entity]):

    def __init__(
        self,
        database_url: str,
        mapping: ModelMapping[Entity, DbModel],
    ):
        self.connection = PgConnection(database_url)
        self.mapping = mapping

    @override
    async def create_or_update(self, item: Entity) -> UID:
        logger.info(f"{item}")
        async with self.connection.transaction() as session:
            item.last_update_date = datetime.now()
            await session.merge(
                self.mapping.entity_to_model(item),
            )
            return getattr(item, self.mapping.primary_key.name)

    @override
    async def delete_by_id(self, primary_key: UID):
        logger.info(f"{primary_key}")
        async with self.connection.transaction() as session:
            await session.execute(
                delete(self.mapping.model).where(
                    self.mapping.primary_key == primary_key
                )
            )

    @override
    async def find_by_id(self, primary_key: UID):
        async with self.connection.transaction() as session:
            stmt = select(self.mapping.model).where(
                self.mapping.primary_key == primary_key
            )
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                values = self.mapping.extract_dict(row)
                logger.info(f"{self.mapping.model}\n{values}")
                return self.mapping.model_to_entity(
                    row,
                )
            return None

    @override
    async def find_all(self, query: Any | None = None) -> AsyncGenerator[Entity, Any]:
        async with self.connection.transaction() as session:
            result = await session.execute(select(self.mapping.model))
        for row in result.scalars().all():
            yield self.mapping.entity(
                **self.mapping.extract_dict(row),
            )

    @override
    async def init(self):
        await self.connection.init_table(self.mapping.model)

    @override
    async def close(self):
        await self.connection.disconnect()
