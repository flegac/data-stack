from dataclasses import dataclass

from meteo_backend.core.config.settings import Settings
from meteo_domain.core.unit_of_work import UnitOfWork
from meteo_domain.data_file.datafile_service import DataFileService
from meteo_domain.workspace.workspace_service import WorkspaceService


@dataclass
class ApplicationContext:
    settings: Settings
    uow: UnitOfWork
    datafile_service: DataFileService
    ws_service: WorkspaceService

    @classmethod
    def from_container(cls, container):
        return cls(
            settings=container.settings(),
            uow=container.sql_uow(),
            datafile_service=container.datafile_service(),
            ws_service=container.ws_service(),
        )
