from loguru import logger

from measure_repository_datafile.datafile_measure_reader import DataFileMeasureReader
from meteo_measures.entities.data_file import DataFile
from meteo_measures.entities.task_status import TaskStatus
from meteo_measures.ports.data_file_repository import DataFileRepository
from meteo_measures.ports.file_repository import FileRepository
from meteo_measures.services.datafile_messaging_service import DataFileMessagingService


class DataFileIngestionService:
    def __init__(
            self,
            messaging: DataFileMessagingService,
            data_file_repository: DataFileRepository,
            file_repository: FileRepository,
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.messaging = messaging

    async def ingestion_listener(self):
        await self.messaging.ingestion_consumer.listen(self.ingest_file)

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
                    await self.messaging.measure_producer.write_batch(measures)
                item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_success)
            except:
                item = await self.data_file_repository.update_status(item, TaskStatus.ingestion_error)
                raise

            return item
        except:
            await self.messaging.error_handler(item)
            raise
