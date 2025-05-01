import datetime
import logging
import random
from unittest import IsolatedAsyncioTestCase

from config import INFLUX_DB_CONFIG
from measure_repository_influxdb.influxdb_measure_repository import InfluxDbMeasureRepository
from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.measure import Measure
from meteo_measures.domain.entities.measures.period import Period
from meteo_measures.domain.entities.measures.sensor import Sensor


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
                type='temperature',
                location=Location(
                    latitude=43.6043,
                    longitude=1.4437
                )
            )
        ))

    async def test_search(self):
        query = MeasureQuery(
            measure_type='temperature',
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
            ),
        )
        for measures in self.repo.search(query):
            print(measures)
