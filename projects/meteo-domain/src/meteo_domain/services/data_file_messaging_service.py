from functools import cached_property

from loguru import logger
from message_queue.mq_factory import MQFactory

from meteo_domain.config import (
    DATAFILE_ERROR_TOPIC,
    DATAFILE_INGESTION_TOPIC,
    MEASURE_TOPIC,
)
from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.ports.data_file_repository import DataFileRepository


class DataFileMessagingService:
    def __init__(
        self,
        data_file_repository: DataFileRepository,
        mq_factory: MQFactory,
    ):
        self.data_file_repository = data_file_repository
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
    def measure_producer(self):
        return self.mq_factory.producer(MEASURE_TOPIC)

    async def error_handler(self, item: DataFile, error: Exception = None):
        logger.warning(f"_handle_error: {error}: {item}")
        await self.data_file_repository.update_status(
            item, DataFileLifecycle.ingestion_failed
        )
        await self.error_producer.write_single(item)
