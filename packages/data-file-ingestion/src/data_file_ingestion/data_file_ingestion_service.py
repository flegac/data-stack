from pathlib import Path

from loguru import logger

from data_file_repository.data_file import DataFile
from data_file_repository.data_file_repository import DataFileRepository
from data_file_repository.task_status import TaskStatus
from file_repository.file_repository import FileRepository
from message_queue.mq_producer import MQProducer


class DataFileIngestionService:
    def __init__(
            self,
            data_file_repository: DataFileRepository,
            file_repository: FileRepository,
            producer: MQProducer[DataFile]
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.producer = producer

    async def upload_file(self, key: str, path: Path) -> DataFile | None:
        logger.info(f'upload_file: {key}[{path}')
        item = DataFile.from_file(key, path)
        await self.data_file_repository.create_or_update(item)

        try:
            item = await self.data_file_repository.update_status(item, TaskStatus.upload_in_progress)
            await self.file_repository.upload_file(item.key, path.read_bytes())
            item = await self.data_file_repository.update_status(item, TaskStatus.upload_success)
            await self.producer.write_single(item)
            item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_pending)
            return item
        except:
            await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
            raise

    async def ingest_file(self, item: DataFile):
        assert item.status in [TaskStatus.ingestion_pending]

        try:
            item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_in_progress)

            local_path = await self.file_repository.download_file(item.key)
            raise NotImplementedError

            item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_success)
            return item
        except:
            await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
            raise
