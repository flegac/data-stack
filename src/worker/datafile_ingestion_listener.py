from dataclasses import dataclass

from dependency_injector.wiring import Provide
from loguru import logger

from data_file_ingestion.data_file_ingestion_service import DataFileIngestionService


@dataclass
class DataFileIngestionListener:
    service: DataFileIngestionService = Provide['ingestion_service']

    async def run(self):
        logger.debug('DataFileIngestionListener.run')
        await self.service.ingestion_listener()
