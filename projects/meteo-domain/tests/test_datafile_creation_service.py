from datetime import datetime
from unittest import TestCase

from aa_common.constants import EXPORT_PATH, LOCAL_TEST_PATH
from meteo_domain.entities.meta_data_file.coordinate import Coordinate
from meteo_domain.entities.meta_data_file.meta_data_file import MetaDataFile
from meteo_domain.entities.meta_data_file.variable import Variable
from meteo_domain.services.datafile_creation_service import DataFileCreationService


class TestDataFileCreationService(TestCase):
    def setUp(self):
        EXPORT_PATH.mkdir(parents=True, exist_ok=True)
        self.service = DataFileCreationService()

    def test_randomize(self):
        self.service.randomize(
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
