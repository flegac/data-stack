import datetime

from measure_repository.measure_query import MeasureQuery
from measure_repository.model.location import Location
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.period import Period
from measure_repository_openmeteo.open_meteo_measure_reader import OpenMeteoMeasureReader


def main():
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

    for data in OpenMeteoMeasureReader(query).read_all():
        print(data)


if __name__ == '__main__':
    main()
