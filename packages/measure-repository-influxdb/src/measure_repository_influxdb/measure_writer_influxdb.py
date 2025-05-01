from functools import cached_property
from typing import override

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from measure_repository.model.measure import Measure
from measure_repository.model.measure_series import MeasureSeries
from measure_repository.stream.measure_writer import MeasureWriter
from measure_repository_influxdb.influxdb_config import InfluxDBConfig


class InfluxDbMeasureWriter(MeasureWriter):
    def __init__(self, config: InfluxDBConfig):
        self.config = config

    @cached_property
    def client(self):
        return InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org,
        )

    @override
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

    @override
    def write_batch(self, measures: MeasureSeries):
        for _ in measures:
            self.write(_)

    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            del self.__dict__['client']

    @property
    def _write_api(self):
        return self.client.write_api(write_options=SYNCHRONOUS)
