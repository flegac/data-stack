from itertools import islice
from unittest import TestCase

from loguru import logger

from aa_common.constants import DATASET_ROOT_PATH
from meteo_domain.entities.datafile import DataFile
from posix_measure_repository.data_file_measure_repository import (
    DataFileMeasureRepository,
)


class TestInfluDbMeasureIO(TestCase):

    def test_io(self):
        paths = [
            DATASET_ROOT_PATH / "CDS-2025-01.grib",
            DATASET_ROOT_PATH / "CDS-1983-10-22.nc",
            DATASET_ROOT_PATH / "CDS-1983-10.nc",
            DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        ]

        grib = DataFile.from_file(
            path=paths[-1],
            uid="test_io",
        )

        repository = DataFileMeasureRepository(grib)

        provider = islice(repository.search(), 5)

        for measures in provider:
            # max_value = measures.measures["value"].max()
            logger.info(f"{measures}")
