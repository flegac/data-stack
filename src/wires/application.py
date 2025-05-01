from dependency_injector import containers, providers

from meteo_measures.domain.services.data_file_ingestion_service import DataFileIngestionService
from meteo_measures.domain.services.data_file_messaging_service import DataFileMessagingService
from meteo_measures.domain.services.data_file_upload_service import DataFileUploadService
from wires.config import Config
from wires.repositories import RepositoryContainer


class ApplicationContainer(containers.DeclarativeContainer):
    repositories = providers.Container(
        RepositoryContainer,
        config=Config
    )

    messaging_service = providers.Singleton(
        DataFileMessagingService,
        data_file_repository=repositories.data_file_repository,
        mq_factory=repositories.mq_factory,
    )
    upload_service = providers.Singleton(
        DataFileUploadService,
        data_file_repository=repositories.data_file_repository,
        file_repository=repositories.file_repository,
        messaging=messaging_service
    )
    ingestion_service = providers.Singleton(
        DataFileIngestionService,
        data_file_repository=repositories.data_file_repository,
        file_repository=repositories.file_repository,
        messaging=messaging_service
    )
