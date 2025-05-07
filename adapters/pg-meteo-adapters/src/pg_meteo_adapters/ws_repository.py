from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.ws_repository import WorkspaceRepository
from pg_connector.model_mapping import ModelMapping
from pg_connector.pg_repository import PgRepository
from pg_meteo_adapters.ws_model import WorkspaceModel


class PgWorkspaceRepository(
    PgRepository[Workspace, WorkspaceModel],
    WorkspaceRepository,
):
    def __init__(self, database_url: str):
        super().__init__(database_url, ModelMapping(Workspace, WorkspaceModel))
