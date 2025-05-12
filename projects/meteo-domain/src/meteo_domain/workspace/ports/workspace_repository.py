from abc import ABC

from aa_common.repo.repository import Repository

from meteo_domain.workspace.entities.workspace import Workspace


class WorkspaceRepository(Repository[Workspace], ABC): ...
