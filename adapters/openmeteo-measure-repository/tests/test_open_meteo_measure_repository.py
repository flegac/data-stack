import datetime
from unittest import IsolatedAsyncioTestCase

from meteo_domain.entities.measures.location import Location
from meteo_domain.entities.measures.measure_query import MeasureQuery
from meteo_domain.entities.measures.period import Period
from openmeteo_measure_repository.open_meteo_measure_repository import (
    OpenMeteoMeasureRepository,
)


class TestInfluDbMeasureRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.repo = OpenMeteoMeasureRepository()

    async def test_search(self):
        query = MeasureQuery(
            measure_type="temperature",
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.UTC),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.UTC),
            ),
            location=Location(latitude=43.6043, longitude=1.4437),
        )
        for measures in self.repo.search(query):
            print(measures)
