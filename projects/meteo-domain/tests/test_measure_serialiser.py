import datetime
from unittest import TestCase

from meteo_domain.entities.geo_spatial.location import Location
from meteo_domain.entities.measurement.measure_serializer import MeasureSerializer
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.sensor import Sensor


class TestMeasureSerializer(TestCase):
    def test_serializer(self):
        serializer = MeasureSerializer()

        sensor = Sensor(
            uid="MySensor",
            measure_type="temperature",
            location=Location(
                latitude=12.3,
                longitude=25.3,
            ),
        )

        item = Measurement(value=33, time=datetime.datetime.now(), sensor=sensor)

        expected = serializer.serialize(item)

        item_back = serializer.deserialize(expected)
        actual = serializer.serialize(item_back)

        print(item)
        print(expected)

        print(item_back)
        print(actual)

        self.assertEqual(expected, actual)
