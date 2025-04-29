from pathlib import Path
from unittest import TestCase

from data_file_repository.data_file import DataFile
from data_file_repository.data_file_serializer import DataFileSerializer


class TestSerializer(TestCase):
    def test_serializer(self):
        serializer = DataFileSerializer()

        item = DataFile.from_file('toto', Path(__file__))

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
