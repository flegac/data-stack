from dependency_injector import containers, providers

from meteo_app.wires.repositories import Repositories
from meteo_domain.services.datafile_messaging_service import DataFileMessagingService
from meteo_domain.services.datafile_service import DataFileService
from meteo_domain.services.workspace_service import WorkspaceService


# pylint: disable=too-few-public-methods
class Services(containers.DeclarativeContainer):
    repositories = providers.Container(Repositories)

    messaging_service = providers.Factory(
        DataFileMessagingService,
        data_file_repository=repositories.data_file_repository,
        mq_factory=repositories.mq_factory,
    )
    datafile_service = providers.Singleton(
        DataFileService,
        data_file_repository=repositories.data_file_repository,
        file_repository=repositories.file_repository,
        messaging=messaging_service,
        measure_repository=repositories.measure_repository,
    )

    ws_service = providers.Singleton(
        WorkspaceService,
        ws_repository=repositories.ws_repository,
        file_repository=repositories.file_repository,
        data_file_repository=repositories.data_file_repository,
    )
