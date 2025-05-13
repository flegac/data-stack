import asyncio
import datetime
from unittest import TestCase

from loguru import logger

from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from influxdb_measure_repository.query_mapping import query_to_flux
from meteo_app.config import INFLUX_DB_CONFIG
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.temporal_series.entities.measure_query import MeasureQuery
from meteo_domain.temporal_series.entities.measurement import (
    TaggedMeasurement,
)
from meteo_domain.temporal_series.entities.period import Period


class TestInfluDbMeasureRepository(TestCase):
    def setUp(self):
        # logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)
        asyncio.run(self.repo.init(reset=True))

        self.sensor = Sensor(
            uid="testing",
            measure_type="something",
            location=Location(latitude=43.6043, longitude=1.4437),
        )

    def measure_generator(self):
        for i in range(10000):
            yield TaggedMeasurement(
                sensor=self.sensor,
                time=datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(seconds=10 * i),
                value=20.0,
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

    def test_save_batch(self):
        asyncio.run(self.repo.save_batch(self.measure_generator()))

    def test_search(self):
        asyncio.run(self.repo.save_batch(self.measure_generator()))

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
