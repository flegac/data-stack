import datetime
import random

from influxdb_connector.measure_influxdb import InfluxDbMeasureRepository
from measure_feature import Measure, MeasureQuery
from measure_feature.model.measure_query import Period
from measure_feature.model.sensor import MeasureType, Location, Sensor
from config import INFLUX_DB_CONFIG


def main():
    measure_influxdb = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)
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
