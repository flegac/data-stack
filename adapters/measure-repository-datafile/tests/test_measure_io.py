from itertools import islice
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from loguru import logger

from measure_repository_datafile.datafile_measure_reader import DataFileMeasureReader
from meteo_measures.entities import DataFile


class TestInfluDbMeasureIO(IsolatedAsyncioTestCase):

    async def test_io(self):
        path = Path.home() / 'Documents' / 'Data' / 'Datasets'
        filepath = path / 'CDS-2025-01.grib'
        filepath = path / 'CDS-1983-10-22.nc'
        filepath = path / 'CDS-1983-10.nc'

        grib = DataFile.from_file(
            path=path / 'CDS-hydro-2020-10-22.nc',
        )

        reader = DataFileMeasureReader(grib)

        provider = islice(reader.read_all(), 5)

        for measures in provider:
            max_value = measures.measures['value'].max()
            logger.debug(
                f'{measures.sensor.id}[{measures.sensor.type.name}]\n{measures.sensor.location}\n{measures.measures.head()}')
