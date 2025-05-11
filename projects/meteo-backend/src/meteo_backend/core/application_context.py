from dataclasses import dataclass

from meteo_backend.core.config.settings import Settings
from meteo_domain.services.datafile_messaging_service import DataFileMessagingService
from meteo_domain.services.datafile_service import DataFileService
from meteo_domain.services.workspace_service import WorkspaceService


@dataclass
class ApplicationContext:
    settings: Settings
    datafile_service: DataFileService
    messaging_service: DataFileMessagingService
    ws_service: WorkspaceService

    @classmethod
    def from_container(cls, container):
        return cls(
            settings=container.settings(),
            datafile_service=container.datafile_service(),
            messaging_service=container.messaging_service(),
            ws_service=container.ws_service(),
        )
