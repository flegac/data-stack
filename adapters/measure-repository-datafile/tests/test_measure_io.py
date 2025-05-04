from itertools import islice
from unittest import IsolatedAsyncioTestCase

from aa_common.constants import DATASET_ROOT_PATH
from loguru import logger
from measure_repository_datafile.data_file_measure_reader import DataFileMeasureReader
from meteo_domain.entities.data_file import DataFile


class TestInfluDbMeasureIO(IsolatedAsyncioTestCase):
    async def test_io(self):
        paths = [
            DATASET_ROOT_PATH / "CDS-2025-01.grib",
            DATASET_ROOT_PATH / "CDS-1983-10-22.nc",
            DATASET_ROOT_PATH / "CDS-1983-10.nc",
            DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        ]

        grib = DataFile.from_file(path=paths[-1])

        reader = DataFileMeasureReader(grib)

        provider = islice(reader.read_all(), 5)

        for measures in provider:
            # max_value = measures.measures["value"].max()
            logger.info(
                f"{measures.sensor.id}[{measures.sensor.type.name}]\n"
                f"{measures.sensor.location}\n{measures.measures.head()}"
            )
