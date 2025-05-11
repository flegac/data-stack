from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.ws_repository import WorkspaceRepository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository
from sql_meteo_adapters.workspace_model import WorkspaceModel


class SqlWorkspaceRepository(
    SqlRepository[Workspace, WorkspaceModel],
    WorkspaceRepository,
):
    def __init__(self, connection: SqlConnection):
        super().__init__(connection, ModelMapping(Workspace, WorkspaceModel))
