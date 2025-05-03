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

    async def upload_single(self, path: Path) -> DataFile | None:
        item = DataFile.from_file(path)
        logger.info(
            f"upload_file: {item.data_id}\n"
            f"path: {item.local_path}\n"
            f"hash:{item.source_hash}"
        )
        await self.data_file_repository.create_or_update(item)

        try:
            await self.data_file_repository.update_status(
                item, DataFileLifecycle.upload_in_progress
            )
            await self.file_repository.upload_file(
                item.data_id, item.local_path.read_bytes()
            )
            await self.data_file_repository.update_status(
                item, DataFileLifecycle.upload_completed
            )
            await self.messaging.ingestion_producer.write_single(item)
            return item
        except Exception as e:
            await self.messaging.error_handler(item, e)
            raise e
