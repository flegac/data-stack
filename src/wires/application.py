from dependency_injector import containers, providers

from data_file_ingestion.data_file_ingestion_service import DataFileIngestionService
from wires.config import Config
from wires.repositories import RepositoryContainer


class ApplicationContainer(containers.DeclarativeContainer):
    repositories = providers.Container(
        RepositoryContainer,
        config=Config
    )

    ingestion_service = providers.Singleton(
        DataFileIngestionService,
        data_file_repository=repositories.data_file_repository,
        file_repository=repositories.file_repository,
        mq_factory=repositories.mq_factory,
    )
