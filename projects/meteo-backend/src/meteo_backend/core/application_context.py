from dataclasses import dataclass

from meteo_domain.data_file.datafile_service import DataFileService
from meteo_domain.workspace.workspace_service import WorkspaceService

from meteo_backend.core.config.settings import Settings


@dataclass
class ApplicationContext:
    settings: Settings
    datafile_service: DataFileService
    ws_service: WorkspaceService

    @classmethod
    def from_container(cls, container):
        return cls(
            settings=container.settings(),
            datafile_service=container.datafile_service(),
            ws_service=container.ws_service(),
        )
