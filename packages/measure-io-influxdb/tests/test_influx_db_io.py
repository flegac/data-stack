import datetime
import random

from config import INFLUX_DB_CONFIG
from measure_io.measure import Measure
from measure_io.measure_query import Period, MeasureQuery
from measure_io.sensor import MeasureType, Location, Sensor
from measure_io_influxdb.measure_reader_influxdb import InfluxDbMeasureReader
from measure_io_influxdb.measure_writer_influxdb import InfluxDbMeasureWriter


def main():
    writer = InfluxDbMeasureWriter(INFLUX_DB_CONFIG)

    writer.write(Measure(
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
    writer.close()

    reader = InfluxDbMeasureReader(INFLUX_DB_CONFIG, MeasureQuery(
        measure_type=MeasureType.TEMPERATURE,
        period=Period(
            start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
        ),
    ))
    for measures in reader.read_all():
        print(measures)
    reader.close()


if __name__ == "__main__":
    main()
