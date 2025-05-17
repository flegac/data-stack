from datetime import datetime
from unittest import TestCase

from datafile_api_xarray.xarray_datafile_api import XarrayDatafileAPI
from meteo_domain.config import EXPORT_PATH, LOCAL_TEST_PATH, DATASET_ROOT_PATH
from meteo_domain.core.logger import logger
from meteo_domain.datafile_ingestion.entities.coordinate import Coordinate
from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.meta_data_file import MetaDataFile
from meteo_domain.datafile_ingestion.entities.variable import Variable


class TestXarrayDataFileAPI(TestCase):
    def setUp(self):
        EXPORT_PATH.mkdir(parents=True, exist_ok=True)
        self.api = XarrayDatafileAPI()

    def test_it(self):
        grib = DataFile.from_file(
            path=DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        )
        data = self.api.load_raw_data(grib)
        logger.info(data)

        data.to_netcdf(EXPORT_PATH / "data.h5")
        data.to_dataframe().to_csv(EXPORT_PATH / "data.csv")

        xxx = DataFile.from_file(EXPORT_PATH / "data.h5")
        xxx_data = self.api.load_raw_data(xxx)

        logger.info(xxx_data)

    def test_randomize(self):
        self.api.randomize(
            MetaDataFile(
                metadata={
                    "sensor_id": "test",
                    "sensor_type": "measures",
                },
                coords=[
                    Coordinate(
                        "time", [datetime(2023, 10, 1, hour, 0) for hour in range(24)]
                    ),
                    Coordinate("latitude", list(range(3))),
                    Coordinate("longitude", list(range(6))),
                ],
                variables=[
                    Variable("temperature", ["time", "latitude", "longitude"]),
                    Variable("pression", ["latitude", "longitude"]),
                ],
            ),
            output_file=LOCAL_TEST_PATH / "random.grib",
        )
