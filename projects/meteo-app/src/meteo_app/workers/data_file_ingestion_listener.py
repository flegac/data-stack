from dataclasses import dataclass

from dependency_injector.wiring import Provide
from meteo_domain.services.data_file_ingestion_service import (
    DataFileIngestionService,
)


@dataclass
class DataFileIngestionListener:
    service: DataFileIngestionService = Provide["ingestion_service"]

    async def run(self):
        await self.service.ingestion_listener()
