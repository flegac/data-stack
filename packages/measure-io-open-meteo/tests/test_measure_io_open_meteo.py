import datetime

from measure_io.measure_query import Period, MeasureQuery
from measure_io.sensor import MeasureType, Location
from measure_io_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader


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
