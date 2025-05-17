from sqlalchemy import Column, String, Date, func

from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_connection import BaseModel, SqlConnection
from sql_connector.sql_repository import SqlRepository
from unit_of_work_sql.patches.location_patch import LocationPatch


class WorkspaceModel(BaseModel):
    __tablename__ = "workspaces"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())


WorkspaceMapper = ModelMapper(Workspace, WorkspaceModel, patches=[LocationPatch()])


class SqlWorkspaceRepository(SqlRepository[Workspace, WorkspaceModel]):
    def __init__(self, connection: SqlConnection):
        super().__init__(connection, WorkspaceMapper)
