import datetime
from unittest import TestCase

from measure_feature import MeasureQuery
from measure_feature.model.measure_query import Period
from measure_feature.model.sensor import MeasureType, Location
from measure_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader


class TestMeasureOpenMeteo(TestCase):

    def test_search(self):
        query = MeasureQuery(
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

        datasource = OpenMeteoMeasureReader(query)
        for data in datasource.read_all():
            print(data.measures.head(20))
