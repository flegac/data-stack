import datetime
from unittest import TestCase

from measure_open_meteo.measure_open_meteo import MeasureOpenMeteo
from measure_repository import MeasureQuery
from measure_repository.model.location import Location
from measure_repository.model.measure_query import Period
from measure_repository.model.measure_type import MeasureType


class TestMeasureOpenMeteo(TestCase):

    def test_search(self):
        datasource = MeasureOpenMeteo()
        data = datasource.search(
            MeasureQuery(
                measure_type=MeasureType.TEMPERATURE,
                period=Period(
                    start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
                    end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
                ),
                location=Location(
                    latitude=43.6043,
                    longitude=1.4437
                ),
            )
        )
        print(data.values.head(20))
