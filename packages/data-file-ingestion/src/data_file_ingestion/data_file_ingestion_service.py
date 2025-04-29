from pathlib import Path

from data_file_repository.data_file import DataFile
from data_file_repository.data_file_repository import DataFileRepository
from data_file_repository.task_status import TaskStatus
from file_repository_s3.s3_file_repository import S3FileRepository
from kafka_connector.kafka_producer import KafkaProducer


class DataFileIngestionService:
    def __init__(
            self,
            data_file_repository: DataFileRepository,
            s3_repository: S3FileRepository,
            producer: KafkaProducer[DataFile]
    ):
        self.data_file_repository = data_file_repository
        self.s3_repository = s3_repository
        self.producer = producer

    async def upload_file(self, path: Path):
        item = DataFile.from_file(path)
        await self.data_file_repository.create_or_update(item)

        try:
            await self.data_file_repository.update_status(item.file_uid, TaskStatus.upload_in_progress)
            await self.s3_repository.upload_file(item.name, path.read_bytes())
            await self.data_file_repository.update_status(item.file_uid, TaskStatus.upload_success)
            await self.producer.write_single(item)
            await self.data_file_repository.update_status(item.file_uid, TaskStatus.ingestion_pending)
        except:
            await self.data_file_repository.update_status(item.file_uid, TaskStatus.ingestion_error)

    async def ingest_file(self, item: DataFile):
        assert item.status in [TaskStatus.ingestion_pending]

        try:
            await self.data_file_repository.update_status(item, TaskStatus.ingestion_in_progress)

            local_path = await self.s3_repository.download_file(item.file_uid)


            await self.data_file_repository.update_status(item, TaskStatus.ingestion_success)
        except:
            await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
