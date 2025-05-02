from itertools import islice
from unittest import IsolatedAsyncioTestCase

from loguru import logger

from aa_common.constants import DATASET_ROOT_PATH
from measure_repository_datafile.data_file_measure_reader import DataFileMeasureReader
from meteo_measures.domain.entities.data_file import DataFile


class TestInfluDbMeasureIO(IsolatedAsyncioTestCase):

    async def test_io(self):
        filepath = DATASET_ROOT_PATH / 'CDS-2025-01.grib'
        filepath = DATASET_ROOT_PATH / 'CDS-1983-10-22.nc'
        filepath = DATASET_ROOT_PATH / 'CDS-1983-10.nc'

        grib = DataFile.from_file(
            path=DATASET_ROOT_PATH / 'CDS-hydro-2020-10-22.nc',
        )

        reader = DataFileMeasureReader(grib)

        provider = islice(reader.read_all(), 5)

        for measures in provider:
            max_value = measures.measures['value'].max()
            logger.debug(
                f'{measures.sensor.id}[{measures.sensor.type.name}]\n{measures.sensor.location}\n{measures.measures.head()}')
