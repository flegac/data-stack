import datetime
import random
from unittest import IsolatedAsyncioTestCase

from config import INFLUX_DB_CONFIG
from measure_repository_influxdb.measure_reader_influxdb import InfluxDbMeasureReader
from measure_repository_influxdb.measure_writer_influxdb import InfluxDbMeasureWriter
from meteo_measures.entities import Location
from meteo_measures.entities import Measure
from meteo_measures.entities import MeasureQuery
from meteo_measures.entities import MeasureType
from meteo_measures.entities import Sensor
from meteo_measures.entities.measures.period import Period


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
