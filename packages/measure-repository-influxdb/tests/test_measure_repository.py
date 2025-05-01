import datetime
import logging
import random
from unittest import IsolatedAsyncioTestCase

from config import INFLUX_DB_CONFIG
from measure_repository.measure_query import MeasureQuery
from measure_repository.model.location import Location
from measure_repository.model.measure import Measure
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.period import Period
from measure_repository.model.sensor import Sensor
from measure_repository_influxdb.influxdb_measure_repository import InfluxDbMeasureRepository


class TestInfluDbMeasureRepository(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        self.repo = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)

    async def test_save(self):
        self.repo.save(Measure(
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

    async def test_search(self):
        query = MeasureQuery(
            measure_type=MeasureType.TEMPERATURE,
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
            ),
        )
        for measures in self.repo.search(query):
            print(measures)
