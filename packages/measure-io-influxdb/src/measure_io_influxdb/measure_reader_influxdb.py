from collections import defaultdict
from functools import cached_property
from typing import Generator, Any

from influxdb_client import InfluxDBClient

from measure_io.measure import Measure, MeasureSeries
from measure_io.measure_query import MeasureQuery
from measure_io.measure_reader import MeasureReader
from measure_io.sensor import Sensor, MeasureType, SensorId
from measure_io_influxdb.influxdb_config import InfluxDBConfig


class InfluxDbMeasureReader(MeasureReader):

    def __init__(self, config: InfluxDBConfig, query: MeasureQuery):
        self.config = config
        self.query = query

    @cached_property
    def client(self):
        return InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org,
        )

    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        flux_query = query_to_flux(query=self.query, bucket=self.config.bucket)
        tables = self._query_api.query(flux_query, org=self.config.org)

        sensors: dict[SensorId, Sensor] = {}
        measure_series: dict[SensorId, list[Measure]] = defaultdict(list)

        for table in tables:
            for record in table.records:
                sensor = Sensor(
                    id=record.values['sensor_id'],
                    type=MeasureType[record.values['_measurement'].upper()],
                    # location=Location(
                    #     latitude=record['latitude'],
                    #     longitude=record['longitude'],
                    #     altitude=record['altitude']
                    # )
                )
                sensors[sensor.id] = sensor
                measure_series[sensor.id].append(Measure(
                    datetime=record.values['_time'],
                    value=record.values['_value'],
                ))

        for sensor_id, measures in measure_series.items():
            yield MeasureSeries.from_measures(sensors[sensor_id], measures)

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            del self.__dict__['client']

    @property
    def _query_api(self):
        return self.client.query_api()


def query_to_flux(query: MeasureQuery, bucket: str):
    if query.location:
        raise NotImplementedError('location is not supported')

    return f"""from(bucket: "{bucket}")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "{query.measure_type.name.lower()}")"""
