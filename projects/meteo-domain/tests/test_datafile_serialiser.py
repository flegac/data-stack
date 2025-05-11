from unittest import TestCase

from aa_common.constants import DATASET_ROOT_PATH
from aa_common.logger import logger
from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.datafile_serializer import DataFileSerializer


class TestDataFileSerializer(TestCase):
    def test_serializer(self):
        serializer = DataFileSerializer()

        item = DataFile.from_file(
            path=DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        )
        logger.info(item.metadata)

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        logger.info(item)
        logger.info(expected)

        logger.info(item_back)
        logger.info(actual)

        self.assertEqual(expected, actual)
