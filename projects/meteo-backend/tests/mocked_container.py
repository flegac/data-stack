from pathlib import Path
from unittest.mock import AsyncMock

from dependency_injector import containers, providers

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.config.settings import Settings
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.ports.measure_repository import MeasureRepository
from meteo_domain.services.data_file_messaging_service import DataFileMessagingService
from meteo_domain.services.data_file_upload_service import DataFileUploadService


class MockedContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = providers.Singleton(
        Settings, LOCAL_STORAGE_PATH=Path("/tmp/test-meteo-files")
    )

    # Mock repositories
    file_repository = providers.Singleton(AsyncMock, spec=FileRepository)
    data_file_repository = providers.Singleton(AsyncMock, spec=DataFileRepository)
    measure_repository = providers.Singleton(AsyncMock, spec=MeasureRepository)

    # Mock messaging service
    messaging_service = providers.Singleton(
        AsyncMock,
        spec=DataFileMessagingService,
    )

    # Service d'Upload avec des dépendances mockées
    file_service = providers.Singleton(
        DataFileUploadService,
        messaging=messaging_service,
        file_repository=file_repository,
        data_file_repository=data_file_repository,
    )

    # Application context
    context = providers.Singleton(
        ApplicationContext,
        settings=settings,
        file_service=file_service,
        ingestion_service=providers.Singleton(AsyncMock),
        messaging_service=messaging_service,
    )
