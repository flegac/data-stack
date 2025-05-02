from pathlib import Path

from loguru import logger
from meteo_measures.domain.entities.data_file import DataFile
from meteo_measures.domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_measures.domain.ports.data_file_repository import DataFileRepository
from meteo_measures.domain.ports.file_repository import FileRepository
from meteo_measures.domain.services.data_file_messaging_service import (
    DataFileMessagingService,
)


class DataFileUploadService:
    def __init__(
        self,
        messaging: DataFileMessagingService,
        data_file_repository: DataFileRepository,
        file_repository: FileRepository,
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.messaging = messaging

    async def upload_file(self, path: Path, key: str | None = None) -> DataFile | None:
        logger.info(f"upload_file: {key}[{path}")
        item = DataFile.from_file(path=path, key=key)
        await self.data_file_repository.create_or_update(item)

        try:
            item = await self.data_file_repository.update_status(
                item, DataFileLifecycle.upload_in_progress
            )
            await self.file_repository.upload_file(item.key, path.read_bytes())
            item = await self.data_file_repository.update_status(
                item, DataFileLifecycle.upload_completed
            )
            await self.messaging.ingestion_producer.write_single(item)
            return item
        except Exception:
            await self.messaging.error_handler(item)
            raise
