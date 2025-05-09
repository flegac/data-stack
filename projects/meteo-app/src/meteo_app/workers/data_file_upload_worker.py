from dataclasses import dataclass
from pathlib import Path

from dependency_injector.wiring import Provide
from meteo_domain.services.data_file_upload_service import DataFileUploadService


@dataclass
class DataFileUploadWorker:
    datafile_path: Path
    service: DataFileUploadService = Provide["upload_service"]

    async def run(self):
        await self.service.upload_single(self.datafile_path)
