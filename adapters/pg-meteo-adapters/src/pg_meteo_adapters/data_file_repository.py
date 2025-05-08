from collections.abc import AsyncGenerator
from typing import override

from meteo_domain.entities.data_file import DataFile
from meteo_domain.ports.data_file_repository import DataFileQuery, DataFileRepository
from pg_connector.model_mapping import ModelMapping
from pg_connector.pg_repository import PgRepository
from sqlalchemy.future import select

from pg_meteo_adapters.data_file_model import DataFileModel


class PgDataFileRepository(
    PgRepository[DataFile, DataFileModel],
    DataFileRepository,
):
    def __init__(self, database_url: str):
        super().__init__(database_url, ModelMapping(DataFile, DataFileModel))

    @override
    async def find_all(
        self, query: DataFileQuery | None = None
    ) -> AsyncGenerator[DataFile]:
        model = self.mapping.model
        async with self.connection.transaction() as session:
            q = select(model)
            if query and query.source_hash:
                q = q.where(model.source_hash == query.source_hash)
            if query and query.workspace_id:
                q = q.where(model.workspace_id == query.workspace_id)
            result = await session.execute(q)
        for row in result.scalars().all():
            yield DataFile(
                **self.mapping.extract_dict(row),
            )
