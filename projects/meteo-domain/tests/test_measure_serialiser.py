import datetime
from unittest import TestCase

from meteo_domain.measurement.entities.measurement import Measurement
from meteo_domain.serializers.measurement_serializer import MeasurementSerializer


class TestMeasureSerializer(TestCase):
    def test_serializer(self):
        serializer = MeasurementSerializer()

        item = Measurement(value=33, time=datetime.datetime.now())

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
