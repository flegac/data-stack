import time
from functools import cached_property

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from measure_influxdb.influxdb_config import InfluxDBConfig
from measure_repository import MeasureSeries, Measure, MeasureQuery
from measure_repository.measure_repository import MeasureRepository
from measure_repository.model.sensor import Sensor, MeasureType


class MeasureInfluxDb(MeasureRepository):
    def __init__(self, config: InfluxDBConfig):
        self.config = config

    @cached_property
    def client(self):
        return influxdb_client.InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org,
        )

    def write(self, measure: Measure):
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

    def write_batch(self, measures: MeasureSeries):
        for _ in measures:
            self.write(_)

    def search(self, query: MeasureQuery):
        flux_query = query_to_flux(query=query, bucket=self.config.bucket)
        tables = self._query_api.query(flux_query, org=self.config.org)

        measures = []

        for table in tables:
            for record in table.records:
                measure = Measure(
                    datetime=record.values['_time'],
                    value=record.values['_value'],
                    sensor=Sensor(
                        id=record.values['sensor_id'],
                        type=MeasureType[record.values['_measurement'].upper()],
                        # location=Location(
                        #     latitude=record['latitude'],
                        #     longitude=record['longitude'],
                        #     altitude=record['altitude']
                        # )
                    )
                )
                measures.append(measure)
        return measures

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            del self.__dict__['client']

    @property
    def _write_api(self):
        return self.client.write_api(write_options=SYNCHRONOUS)

    @property
    def _query_api(self):
        return self.client.query_api()

    @property
    def _buckets_api(self):
        return self.client.buckets_api()


def query_to_flux(query: MeasureQuery, bucket: str):
    if query.location:
        raise NotImplementedError('location is not supported')

    return f"""from(bucket: "{bucket}")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "{query.measure_type.name.lower()}")"""
