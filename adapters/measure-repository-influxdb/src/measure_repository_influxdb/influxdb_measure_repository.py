from collections import defaultdict
from collections.abc import Generator, Iterable
from functools import cached_property
from typing import Any, override

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.entities.measures.sensor import Sensor, SensorId
from meteo_domain.ports.measure_repository import MeasureRepository

from measure_repository_influxdb.influxdb_config import InfluxDBConfig


def measure_to_point(measure: Measurement):
    return (
        Point(measure.sensor.type.lower())
        .tag("sensor_id", measure.sensor.id)
        .field("value", measure.value)
    )


class InfluxDbMeasureRepository(MeasureRepository):
    def __init__(self, config: InfluxDBConfig):
        self.config = config

    @override
    async def save(self, measure: Measurement):
        logger.info(f"{measure.sensor}")

        self._write_api.write(
            bucket=self.config.bucket,
            org=self.config.org,
            record=measure_to_point(measure),
        )

    @override
    async def save_batch(self, measures: Iterable[Measurement]):
        records = [measure_to_point(_) for _ in measures]
        logger.info(
            f"org={self.config.org} bucket={self.config.bucket}: {len(records)}"
        )
        self._write_api.write(
            bucket=self.config.bucket, org=self.config.org, record=records
        )

    @override
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]:
        logger.info(f"{query}")
        flux_query = query_to_flux(query=query, bucket=self.config.bucket)
        logger.info(f"flux:\n{flux_query}")
        tables = self._query_api.query(flux_query, org=self.config.org)

        sensors: dict[tuple[SensorId, str], Sensor] = {}
        measure_series: dict[tuple[SensorId, str], list[Measurement]] = defaultdict(
            list
        )

        for table in tables:
            for record in table.records:
                sensor = Sensor(
                    id=record.values["sensor_id"],
                    type=record.values["_measurement"],
                    # location=Location(
                    #     latitude=record['latitude'],
                    #     longitude=record['longitude'],
                    #     altitude=record['altitude']
                    # )
                )
                key = (sensor.id, sensor.type)
                sensors[key] = sensor
                measure_series[key].append(
                    Measurement(
                        datetime=record.values["_time"],
                        value=record.values["_value"],
                    )
                )

        for key, measures in measure_series.items():
            yield MeasureSeries.from_measures(sensors[key], measures)

    def close(self):
        if hasattr(self, "client"):
            self.client.close()
            del self.__dict__["client"]

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
        raise NotImplementedError("location is not supported")

    start_time = "-10m"
    end_time = "now()"
    if query.period:
        if query.period.start:
            start_time = query.period.start.isoformat()
        if query.period.end:
            end_time = query.period.end.isoformat()

    flux_query = f"""from(bucket: "{bucket}")
    |> range(start: {start_time}, stop: {end_time})"""

    if query.measure_type is not None:
        flux_query += (
            f'\n    |> filter(fn: (r) => r._measurement == "{query.measure_type}")'
        )

    if query.tags is not None:
        for tag_key, tag_values in query.tags.items():
            if tag_values:
                flux_query += (
                    f"\n    |> filter("
                    f"fn: (r) => contains(value: r.{tag_key}, set: {tag_values}))"
                )

    return flux_query
