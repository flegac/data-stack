from dataclasses import dataclass

from dependency_injector.wiring import Provide

from meteo_domain.services.datafile_service import (
    DataFileService,
)


@dataclass
class DataFileIngestionListener:
    service: DataFileService = Provide["datafile_service"]

    async def run(self):
        await self.service.start_ingest_listener()
