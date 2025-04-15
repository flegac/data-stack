import datetime
import random

from measure_influxdb.measure_influxdb import MeasureInfluxDb
from measure_repository import Measure, MeasureQuery
from measure_repository.model.measure_query import Period
from measure_repository.model.sensor import MeasureType, Location, Sensor
from src.config import INFLUX_DB_CONFIG


def main():
    measure_influxdb = MeasureInfluxDb(INFLUX_DB_CONFIG)
    measure_influxdb.write(Measure(
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

    measures = measure_influxdb.search(MeasureQuery(
        measure_type=MeasureType.TEMPERATURE,
        period=Period(
            start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
        ),
    ))
    for measure in measures:
        print(measure)

    measure_influxdb.close()


if __name__ == "__main__":
    main()
