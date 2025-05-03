from dataclasses import dataclass

from dependency_injector.wiring import Provide
from loguru import logger
from meteo_measures.domain.services.data_file_ingestion_service import (
    DataFileIngestionService,
)


@dataclass
class DataFileIngestionListener:
    service: DataFileIngestionService = Provide["ingestion_service"]

    async def run(self):
        logger.info("DataFileIngestionListener.run")
        await self.service.ingestion_listener()
