import datetime
import random
from unittest import IsolatedAsyncioTestCase

from config import INFLUX_DB_CONFIG
from measure_repository.measure_query import MeasureQuery
from measure_repository.model.location import Location
from measure_repository.model.measure import Measure
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.period import Period
from measure_repository.model.sensor import Sensor
from measure_repository_influxdb.measure_reader_influxdb import InfluxDbMeasureReader
from measure_repository_influxdb.measure_writer_influxdb import InfluxDbMeasureWriter


class TestInfluDbMeasureIO(IsolatedAsyncioTestCase):

    async def test_io(self):
        writer = InfluxDbMeasureWriter(INFLUX_DB_CONFIG)

        writer.write(Measure(
            datetime=datetime.datetime.now(),
            value=random.random(),
            sensor=Sensor(
                id="test",
                type=MeasureType.TEMPERATURE,
                location=Location(
                    latitude=43.6043,
                    longitude=1.4437
                )
            )
        ))
        writer.close()

        reader = InfluxDbMeasureReader(INFLUX_DB_CONFIG, MeasureQuery(
            measure_type=MeasureType.TEMPERATURE,
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
            ),
        ))
        for measures in reader.read_all():
            print(measures)
        reader.close()
