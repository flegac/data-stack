from pathlib import Path
from unittest.mock import AsyncMock

from dependency_injector import containers, providers
from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.config.settings import Settings
from meteo_domain.core.impl.memory_mq_backend import MemoryMQBackend
from meteo_domain.data_file.datafile_service import DataFileService
from meteo_domain.data_file.ports.data_file_repository import (
    MemDataFileRepository,
)
from meteo_domain.data_file.ports.file_repository import FileRepository
from meteo_domain.temporal_series.ports.tseries_repository import TSeriesRepository


class MockedContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = providers.Singleton(
        Settings, LOCAL_STORAGE_PATH=Path("/tmp/test-meteo-files")
    )

    # Mock repositories
    file_repository = providers.Singleton(AsyncMock, spec=FileRepository)
    data_file_repository = providers.Singleton(MemDataFileRepository)
    measure_repository = providers.Singleton(AsyncMock, spec=TSeriesRepository)

    mq_backend = providers.Singleton(MemoryMQBackend)

    # Service d'Upload avec des dépendances mockées
    datafile_service = providers.Singleton(
        DataFileService,
        mq_backend=mq_backend,
        file_repository=file_repository,
        data_file_repository=data_file_repository,
    )

    # Application context
    context = providers.Singleton(
        ApplicationContext,
        settings=settings,
        datafile_service=datafile_service,
        ws_service=providers.Singleton(AsyncMock),
    )
