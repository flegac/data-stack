from abc import ABC

from meteo_domain.core.repository import Repository
from meteo_domain.workspace.entities.workspace import Workspace


class WorkspaceRepository(Repository[Workspace], ABC): ...
