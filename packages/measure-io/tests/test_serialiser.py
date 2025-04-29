import datetime
from unittest import TestCase

from measure_io.measure import Measure
from measure_io.measure_serializer import MeasureSerializer
from measure_io.sensor import Sensor, MeasureType, Location


class TestSerializer(TestCase):
    def test_serializer(self):
        serializer = MeasureSerializer()

        sensor = Sensor(
            id='MySensor',
            type=MeasureType.TEMPERATURE,
            location=Location(
                latitude=12.3,
                longitude=25.3,
            )
        )

        item = Measure(
            value=33,
            datetime=datetime.datetime.now(),
            sensor=sensor
        )

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
