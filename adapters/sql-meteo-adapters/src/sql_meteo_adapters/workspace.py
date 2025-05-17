from sqlalchemy import Column, String, Date, func

from meteo_domain.ports.workspace_repository import WorkspaceRepository
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.model_mapper import ModelMapper
from sql_connector.patches.location_patch import LocationPatch
from sql_connector.sql_connection import BaseModel
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


class WorkspaceModel(BaseModel):
    __tablename__ = "workspaces"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())


WorkspaceMapper = ModelMapper(Workspace, WorkspaceModel, patches=[LocationPatch()])


class SqlWorkspaceRepository(
    SqlRepository[Workspace, WorkspaceModel],
    WorkspaceRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, WorkspaceMapper)
