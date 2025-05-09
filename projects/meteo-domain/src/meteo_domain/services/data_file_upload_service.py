from pathlib import Path

from loguru import logger

from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.services.data_file_messaging_service import (
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
        logger.info(item)

        if existing := await self.data_file_repository.find_by_id(item.data_id):
            logger.warning(f'"{item.data_id}" already exists:\n{existing}')
        if existing := await self.data_file_repository.find_by_hash(item.source_hash):
            logger.warning(
                f'source_hash "{item.source_hash}" already exists:\n'
                f"{[_.data_id for _ in existing]}"
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
