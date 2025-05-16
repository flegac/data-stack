from datetime import datetime
from unittest import TestCase

from meteo_domain.config import EXPORT_PATH, LOCAL_TEST_PATH
from meteo_domain.metadata_file.entities.coordinate import Coordinate
from meteo_domain.metadata_file.entities.meta_data_file import MetaDataFile
from meteo_domain.metadata_file.entities.variable import Variable
from meteo_domain.metadata_file.metadatafile_service import MetadataFileService


class TestMetadataFileService(TestCase):
    def setUp(self):
        EXPORT_PATH.mkdir(parents=True, exist_ok=True)
        self.service = MetadataFileService()

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
