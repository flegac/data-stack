from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.ports.ws_repository import WorkspaceRepository


class WorkspaceService:
    def __init__(
        self,
        ws_repository: WorkspaceRepository,
        file_repository: FileRepository,
        data_file_repository: DataFileRepository,
    ):
        self.ws_repository = ws_repository
        self.file_repository = file_repository
        self.data_file_repository = data_file_repository

    async def init_workspace(self, ws: Workspace):
        ws = await self.ws_repository.create(ws)
        await self.file_repository.create_bucket(ws.datafile_bucket)

    async def delete_workspace(self, ws: Workspace):
        await self.file_repository.delete_bucket(ws.datafile_bucket)
        await self.ws_repository.delete(ws)

    async def find_data_files(self, ws: Workspace):
        return await self.data_file_repository.find_by_workspace(ws.workspace_id)
