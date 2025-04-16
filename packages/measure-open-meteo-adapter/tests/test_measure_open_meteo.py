import datetime
from unittest import TestCase

from measure_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader
from measure_feature import MeasureQuery
from measure_feature.model.location import Location
from measure_feature.model.measure_query import Period
from measure_feature.model.measure_type import MeasureType


class TestMeasureOpenMeteo(TestCase):

    def test_search(self):
        datasource = OpenMeteoMeasureReader()
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
