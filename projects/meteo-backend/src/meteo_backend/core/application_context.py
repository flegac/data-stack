from dataclasses import dataclass

from meteo_domain.services.data_file_ingestion_service import DataFileIngestionService
from meteo_domain.services.data_file_messaging_service import DataFileMessagingService
from meteo_domain.services.data_file_upload_service import DataFileUploadService

from meteo_backend.core.config.settings import Settings


@dataclass
class ApplicationContext:
    settings: Settings
    file_service: DataFileUploadService
    ingestion_service: DataFileIngestionService
    messaging_service: DataFileMessagingService

    @classmethod
    def from_container(cls, container):
        return cls(
            settings=container.settings(),
            file_service=container.file_service(),
            ingestion_service=container.ingestion_service(),
            messaging_service=container.messaging_service(),
        )
