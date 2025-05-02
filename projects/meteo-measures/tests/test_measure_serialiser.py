import datetime
from unittest import TestCase

from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.measure import Measure
from meteo_measures.domain.entities.measures.measure_serializer import MeasureSerializer
from meteo_measures.domain.entities.measures.sensor import Sensor


class TestMeasureSerializer(TestCase):
    def test_serializer(self):
        serializer = MeasureSerializer()

        sensor = Sensor(
            id="MySensor",
            type="temperature",
            location=Location(
                latitude=12.3,
                longitude=25.3,
            ),
        )

        item = Measure(value=33, datetime=datetime.datetime.now(), sensor=sensor)

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
