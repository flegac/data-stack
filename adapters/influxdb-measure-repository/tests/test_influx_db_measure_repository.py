import asyncio
import datetime
import logging
import random
from unittest import TestCase

from loguru import logger

from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from influxdb_measure_repository.query_mapping import query_to_flux
from meteo_app.config import INFLUX_DB_CONFIG
from meteo_domain.entities.geo_spatial.location import Location
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.sensor import Sensor
from meteo_domain.entities.temporal.period import Period


class TestInfluDbMeasureRepository(TestCase):
    def setUp(self):
        logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)
        self.sensor = Sensor(
            uid="testing",
            measure_type="something",
            location=Location(latitude=43.6043, longitude=1.4437),
        )

    def test_flux_query(self):
        query = MeasureQuery(
            sources=[self.sensor],
            period=Period(
                # start=datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc),
                end=datetime.datetime.now(datetime.UTC)
            ),
            tags={"toto": ["one", "two", "three"], "tata": ["some", "thing"]},
        )
        query_string = query_to_flux(query, "my-bucket")
        print(query_string)

    def test_save(self):
        asyncio.run(
            self.repo.save(
                Measurement(
                    time=datetime.datetime.now(datetime.UTC),
                    value=random.random(),
                    sensor=self.sensor,
                )
            )
        )

    def test_save_batch(self):
        def measure_generator():
            for i in range(10000):
                yield Measurement(
                    time=datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(seconds=10 * i),
                    value=20.0,
                    sensor=self.sensor,
                )

        asyncio.run(self.repo.save_batch(measure_generator()))

    def test_search(self):
        def measure_generator():
            for i in range(10000):
                yield Measurement(
                    time=datetime.datetime.now(datetime.UTC)
                    + datetime.timedelta(seconds=10 * i),
                    value=20.0,
                    sensor=self.sensor,
                )

        asyncio.run(self.repo.save_batch(measure_generator()))

        query = MeasureQuery(
            sources=[self.sensor],
            period=Period(
                start=datetime.datetime(2025, 1, 1, tzinfo=datetime.UTC),
                # end=datetime.datetime.now(datetime.timezone.utc)
            ),
        )
        results = list(self.repo.search(query))

        logger.info(f"Found {len(results)} results")
        for measures in results:
            logger.info(measures)
