from meteo_domain.workspace.entities.workspace import Workspace
from meteo_domain.workspace.ports.workspace_repository import WorkspaceRepository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository

from sql_meteo_adapters.workspace_model import WorkspaceModel


class SqlWorkspaceRepository(
    SqlRepository[Workspace, WorkspaceModel],
    WorkspaceRepository,
):
    def __init__(self, uow: SqlConnection):
        super().__init__(uow, ModelMapping(Workspace, WorkspaceModel))
