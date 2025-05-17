from unittest import TestCase

from meteo_domain.config import DATASET_ROOT_PATH
from meteo_domain.core.logger import logger
from meteo_domain.serializers.datafile_serializer import DataFileSerializer
from meteo_domain.datafile_ingestion.entities.datafile import DataFile


class TestDataFileSerializer(TestCase):
    def test_serializer(self):
        serializer = DataFileSerializer()

        item = DataFile.from_file(
            path=DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        )

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        logger.info(item)
        logger.info(expected)

        logger.info(item_back)
        logger.info(actual)

        self.assertEqual(expected, actual)
