from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from meteo_domain.datafile_ingestion.ports.uow.file_repository import FileRepository
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork


class WorkspaceService:
    def __init__(
        self,
        uow: UnitOfWork,
        file_repository: FileRepository,
    ):
        self.uow = uow
        self.file_repository = file_repository

    async def init_workspace(self, ws: Workspace):
        async with self.uow.transaction():
            await self.uow.workspaces().save(ws)
        await self.file_repository.create_bucket(ws.datafile_bucket)

    async def delete_workspace(self, ws: Workspace):
        await self.file_repository.delete_bucket(ws.datafile_bucket)
        async with self.uow.transaction():
            await self.uow.workspaces().delete_by_id(ws.uid)

    async def find_data_files(self, ws: Workspace):
        async with self.uow.transaction():
            return self.uow.datafiles().find_all(workspace_id=ws.uid)
