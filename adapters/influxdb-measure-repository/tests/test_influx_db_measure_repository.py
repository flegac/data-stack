import datetime
import logging
import random
from unittest import IsolatedAsyncioTestCase

from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from influxdb_measure_repository.query_mapping import query_to_flux
from loguru import logger
from meteo_app.config import INFLUX_DB_CONFIG
from meteo_domain.entities.measures.location import Location
from meteo_domain.entities.measures.measure_query import MeasureQuery
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.entities.measures.period import Period
from meteo_domain.entities.measures.sensor import Sensor


class TestInfluDbMeasureRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)

    async def test_flux_query(self):
        query = MeasureQuery(
            sensor_id="testing",
            measure_type="something",
            period=Period(
                # start=datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc),
                end=datetime.datetime.now(datetime.UTC)
            ),
            tags={"toto": ["one", "two", "three"], "tata": ["some", "thing"]},
        )
        query_string = query_to_flux(query, "my-bucket")
        print(query_string)

    async def test_save(self):
        await self.repo.save(
            Measurement(
                datetime=datetime.datetime.now(),
                value=random.random(),
                sensor=Sensor(
                    id="testing",
                    type="something",
                    location=Location(latitude=43.6043, longitude=1.4437),
                ),
            )
        )

    async def test_save_batch(self):
        measures = MeasureSeries.from_measures(
            sensor=Sensor(
                id="testing",
                type="something",
                location=Location(latitude=43.6043, longitude=1.4437),
            ),
            measures=[
                Measurement(
                    datetime=datetime.datetime.now()
                    + datetime.timedelta(seconds=10 * i),
                    value=20.0,
                )
                for i in range(1000)
            ],
        )
        await self.repo.save_batch(measures)

    async def test_search(self):
        query = MeasureQuery(
            sensor_id="testing",
            # measure_type='something',
            period=Period(
                start=datetime.datetime(2025, 1, 1, tzinfo=datetime.UTC),
                # end=datetime.datetime.now(datetime.timezone.utc)
            ),
        )
        for measures in self.repo.search(query):
            logger.info(measures)
