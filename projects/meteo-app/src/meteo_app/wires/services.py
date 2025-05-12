from dependency_injector import containers, providers
from meteo_domain.data_file.datafile_service import DataFileService
from meteo_domain.workspace.workspace_service import WorkspaceService

from meteo_app.wires.repositories import Repositories


# pylint: disable=too-few-public-methods
class Services(containers.DeclarativeContainer):
    repositories = providers.Container(Repositories)

    datafile_service = providers.Singleton(
        DataFileService,
        data_file_repository=repositories.data_file_repository,
        file_repository=repositories.file_repository,
        mq_backend=repositories.mq_factory,
        measure_repository=repositories.measure_repository,
    )

    ws_service = providers.Singleton(
        WorkspaceService,
        ws_repository=repositories.ws_repository,
        file_repository=repositories.file_repository,
        data_file_repository=repositories.data_file_repository,
    )
