from dataclasses import dataclass
from pathlib import Path

from dependency_injector.wiring import Provide
from loguru import logger

from meteo_measures.services.datafile_upload_servicee import DataFileUploadService


@dataclass
class DataFileUploadWorker:
    service: DataFileUploadService = Provide['upload_service']

    async def run(self):
        path = Path.home() / 'Documents' / 'Data' / 'Datasets'
        filepath = path / 'CDS-2025-01.grib'
        filepath = path / 'CDS-1983-10-22.nc'
        filepath = path / 'CDS-1983-10.nc'

        filepath = path / 'CDS-hydro-2020-10-22.nc'

        item = await self.service.upload_file(filepath)
        logger.debug(f'{item}')
