import asyncio
import datetime
from unittest import TestCase

import numpy as np
from loguru import logger
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from measure_repository_influxdb.query_mapping import query_to_flux
from meteo_app.config import INFLUX_DB_CONFIG
from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.location.location import Location
from meteo_domain.geo_sensor.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.geo_sensor.entities.telemetry.telemetries import Telemetries
from meteo_domain.geo_sensor.entities.times.period import Period


class TestInfluDbMeasureRepository(TestCase):
    def setUp(self):
        # logging.getLogger("asyncio").setLevel(logging.ERROR)
        self.repo = InfluxDbTSeriesRepository(INFLUX_DB_CONFIG)
        asyncio.run(self.repo.init(reset=True))

        self.sensor = GeoSensor(
            uid="testing",
            measure_type="something",
            location=Location(latitude=43.6043, longitude=1.4437),
        )

    def measure_generator(self):
        n = 10_000
        period = Period.from_duration(
            start=datetime.datetime.now(datetime.UTC),
            duration=datetime.timedelta(days=100),
        )
        return Telemetries(
            sensors=[self.sensor for _ in range(n)],
            times=period.split(n),
            values=np.array(
                [20.0 for _ in range(n)],
            ),
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
        asyncio.run(self.repo.save_batch(self.measure_generator().iter()))

    def test_search(self):
        asyncio.run(self.repo.save_batch(self.measure_generator().iter()))

        query = MeasureQuery(
            sources=[self.sensor],
            period=Period(
                start=datetime.datetime(2025, 1, 1, tzinfo=datetime.UTC),
                # end=datetime.datetime.now(datetime.timezone.utc)
            ),
        )
        regions = self.repo.search(query)

        logger.info(f"Found {len(regions.series)} regions")
        for measures in regions.iter_timeline():
            logger.info(str(measures))
