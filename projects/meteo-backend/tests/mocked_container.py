from pathlib import Path
from unittest.mock import AsyncMock

from dependency_injector import containers, providers

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.config.settings import Settings
from meteo_domain.core.impl.memory_mq_backend import MemoryMQBackend
from meteo_domain.datafile_ingestion.datafile_service import DataFileService
from meteo_domain.datafile_ingestion.ports.uow.file_repository import FileRepository
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork
from meteo_domain.measurement.ports.tseries_repository import TSeriesRepository


class MockedContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = providers.Singleton(
        Settings, LOCAL_STORAGE_PATH=Path("/tmp/test-meteo-files")
    )

    # Mock repositories
    uow = providers.Singleton(AsyncMock, spec=UnitOfWork)
    file_repository = providers.Singleton(AsyncMock, spec=FileRepository)
    measure_repository = providers.Singleton(AsyncMock, spec=TSeriesRepository)

    mq_backend = providers.Singleton(MemoryMQBackend)

    # Service d'Upload avec des dépendances mockées
    datafile_service = providers.Singleton(
        DataFileService,
        uow=uow,
        mq_backend=mq_backend,
        file_repository=file_repository,
    )

    # Application context
    context = providers.Singleton(
        ApplicationContext,
        settings=settings,
        datafile_service=datafile_service,
        ws_service=providers.Singleton(AsyncMock),
    )
