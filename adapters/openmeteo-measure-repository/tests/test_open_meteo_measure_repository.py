import datetime
from unittest import TestCase

from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.temporal_series.entities.measure_query import MeasureQuery
from meteo_domain.temporal_series.entities.period import Period
from openmeteo_measure_repository.open_meteo_measure_repository import (
    OpenMeteoMeasureRepository,
)


class TestInfluDbMeasureRepository(TestCase):
    def setUp(self):
        self.repo = OpenMeteoMeasureRepository()

    def test_search(self):
        query = MeasureQuery(
            sources=[
                Sensor(
                    uid="open-meteo",
                    measure_type="temperature",
                    location=Location(latitude=43.6043, longitude=1.4437),
                ),
            ],
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.UTC),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.UTC),
            ),
        )
        for measures in self.repo.search(query):
            print(measures)
