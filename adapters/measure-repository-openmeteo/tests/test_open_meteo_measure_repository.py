import datetime
from unittest import TestCase

from measure_repository_openmeteo.open_meteo_measure_repository import (
    OpenMeteoMeasureRepository,
)
from meteo_domain.measurement.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.measurement.entities.period import Period
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor


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
