import datetime
import random

from measure_influxdb.influxdb_config import InfluxDBConfig
from measure_influxdb.measure_influxdb import InfluxDbConnection
from measure_repository import Measure, MeasureQuery
from measure_repository.model.measure_query import Period
from measure_repository.model.sensor import MeasureType, Location, Sensor

INFLUX_DB_CONFIG = InfluxDBConfig(
    url="http://localhost:8086",
    org="myorg",
    token='k5OmUjRQ0R-unlkmdwoGIV4aYNSqUyfG3uY2I7y1VqIQy5jcE_ErXYQ4b-Epq8BzrmrUwIw1a0zIZV6FCqgd8g==',
    bucket="meteo-data"
)


def main():
    influxdb_repository = InfluxDbConnection(INFLUX_DB_CONFIG)
    influxdb_repository.write(Measure(
        datetime=datetime.datetime.now(),
        value=random.random(),
        sensor=Sensor(
            id="test",
            type=MeasureType.TEMPERATURE,
            location=Location(
                latitude=43.6043,
                longitude=1.4437
            )
        )
    ))

    measures = influxdb_repository.search(MeasureQuery(
        measure_type=MeasureType.TEMPERATURE,
        period=Period(
            start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
        ),
    ))
    for measure in measures:
        print(measure)

    influxdb_repository.close()


if __name__ == "__main__":
    main()
