from functools import cached_property
from pathlib import Path

from loguru import logger

from data_file_ingestion.config import DATAFILE_INGESTION_TOPIC, DATAFILE_ERROR_TOPIC, MEASURE_TOPIC
from data_file_repository.data_file import DataFile
from data_file_repository.data_file_repository import DataFileRepository
from data_file_repository.task_status import TaskStatus
from file_repository.file_repository import FileRepository
from measure_io_datafile.datafile_measure_reader import DataFileMeasureReader
from message_queue.mq_factory import MQFactory


class DataFileIngestionService:
    def __init__(
            self,
            data_file_repository: DataFileRepository,
            file_repository: FileRepository,
            mq_factory: MQFactory,
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.mq_factory = mq_factory

    @cached_property
    def ingestion_producer(self):
        return self.mq_factory.producer(DATAFILE_INGESTION_TOPIC)

    @cached_property
    def ingestion_consumer(self):
        return self.mq_factory.consumer(DATAFILE_INGESTION_TOPIC)

    @cached_property
    def error_producer(self):
        return self.mq_factory.producer(DATAFILE_ERROR_TOPIC)

    @cached_property
    def error_consumer(self):
        return self.mq_factory.consumer(DATAFILE_ERROR_TOPIC)

    @cached_property
    def measure_producer(self):
        return self.mq_factory.producer(MEASURE_TOPIC)

    async def upload_file(self, path: Path, key: str | None = None) -> DataFile | None:
        logger.info(f'upload_file: {key}[{path}')
        item = DataFile.from_file(path=path, key=key)
        await self.data_file_repository.create_or_update(item)

        try:
            item = await self.data_file_repository.update_status(item, TaskStatus.upload_in_progress)
            await self.file_repository.upload_file(item.key, path.read_bytes())
            item = await self.data_file_repository.update_status(item, TaskStatus.upload_success)

            await self.ingestion_producer.write_single(item)
            item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_pending)

            return item
        except:
            await self._handle_error(item)
            raise

    async def ingestion_listener(self):
        await self.ingestion_consumer.listen(self.ingest_file)

    async def ingest_file(self, item: DataFile):
        logger.debug(f'ingest_file: {item}')
        try:
            assert item.status in [TaskStatus.upload_success, TaskStatus.ingestion_pending]

            item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_in_progress)

            item.local_path = await self.file_repository.download_file(item.key)

            reader = DataFileMeasureReader(item)
            provider = reader.read_all()

            try:
                for measures in provider:
                    await self.measure_producer.write_batch(measures)
                item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_success)
            except:
                item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
                raise

            return item
        except:
            await self._handle_error(item)
            raise

    async def _handle_error(self, item):
        logger.warning(f'_handle_error: {item}')
        await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
        await self.error_producer.write_single(item)
