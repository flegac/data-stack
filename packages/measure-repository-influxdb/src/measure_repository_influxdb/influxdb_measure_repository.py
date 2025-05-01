from collections import defaultdict
from functools import cached_property
from typing import Generator, Any, override

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from measure_repository.measure_query import MeasureQuery
from measure_repository.measure_repository import MeasureRepository
from measure_repository.model.measure import Measure
from measure_repository.model.measure_series import MeasureSeries
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.sensor import Sensor, SensorId
from measure_repository_influxdb.influxdb_config import InfluxDBConfig


class InfluxDbMeasureRepository(MeasureRepository):

    def __init__(self, config: InfluxDBConfig):
        self.config = config

    @override
    def save(self, measure: Measure):
        record = (
            Point(measure.sensor.type.name.lower())
            .tag('sensor_id', measure.sensor.id)
            .field('value', measure.value)
        )
        self._write_api.write(
            bucket=self.config.bucket,
            org=self.config.org,
            record=record
        )

    @override
    async def save_batch(self, measures: MeasureSeries):
        for _ in measures:
            self.save(_)

    @override
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]:
        flux_query = query_to_flux(query=query, bucket=self.config.bucket)
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

    @cached_property
    def client(self):
        return InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org,
        )

    @property
    def _write_api(self):
        return self.client.write_api(write_options=SYNCHRONOUS)

    @property
    def _query_api(self):
        return self.client.query_api()


def query_to_flux(query: MeasureQuery, bucket: str):
    if query.location:
        raise NotImplementedError('location is not supported')

    return f"""from(bucket: "{bucket}")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "{query.measure_type.name.lower()}")"""
