from dataclasses import dataclass

from aa_common.constants import DATASET_ROOT_PATH
from dependency_injector.wiring import Provide
from loguru import logger
from meteo_measures.domain.services.data_file_upload_service import (
    DataFileUploadService,
)


@dataclass
class DataFileUploadWorker:
    service: DataFileUploadService = Provide["upload_service"]

    async def run(self):
        filepath = DATASET_ROOT_PATH / "CDS-2025-01.grib"
        filepath = DATASET_ROOT_PATH / "CDS-1983-10-22.nc"
        filepath = DATASET_ROOT_PATH / "CDS-1983-10.nc"
        filepath = DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc"

        item = await self.service.upload_file(filepath)
        logger.debug(f"{item}")
