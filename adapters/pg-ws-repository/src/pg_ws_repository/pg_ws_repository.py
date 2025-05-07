from collections.abc import AsyncGenerator
from datetime import datetime
from typing import override

from aa_common.logger import logger
from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.ws_repository import WorkspaceRepository
from pg_connector.pg_connection import PgConnection
from sqlalchemy import delete, select

from pg_ws_repository.ws_model import WorkspaceModel


def extract_dict(item):
    return {
        "workspace_id": item.workspace_id,
        "name": item.name,
    }


class PgWorkspaceRepository(WorkspaceRepository):
    def __init__(self, database_url: str):
        self.connection = PgConnection(database_url)
        self.model = WorkspaceModel

    @override
    async def create_or_update(self, item: Workspace):
        async with self.connection.transaction() as session:
            item.last_update_date = datetime.now()
            await session.merge(
                self.model(
                    **extract_dict(item),
                )
            )

    @override
    async def delete_by_id(self, workspace_id: str):
        logger.info(f"{workspace_id}")
        async with self.connection.transaction() as session:
            await session.execute(
                delete(self.model).where(self.model.workspace_id == workspace_id)
            )

    @override
    async def find_all(self) -> AsyncGenerator[Workspace, None]:
        async with self.connection.transaction() as session:
            result = await session.execute(select(self.model))
        for row in result.scalars().all():
            yield Workspace(
                **extract_dict(row),
            )

    @override
    async def find_by_id(self, workspace_id: str) -> Workspace | None:
        async with self.connection.transaction() as session:
            stmt = select(self.model).where(self.model.workspace_id == workspace_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                return Workspace(
                    **extract_dict(row),
                )
            return None

    @override
    async def init(self):
        await self.connection.init_table(self.model)

    @override
    async def close(self):
        await self.connection.disconnect()
