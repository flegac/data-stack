from pathlib import Path
from unittest import TestCase

from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.data_file_serializer import DataFileSerializer


class TestDataFileSerializer(TestCase):
    def test_serializer(self):
        serializer = DataFileSerializer()

        item = DataFile.from_file(Path(__file__))

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
