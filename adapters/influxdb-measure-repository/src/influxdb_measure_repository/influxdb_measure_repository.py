from collections.abc import Generator, Iterable
from typing import override

from influxdb_connector.influx_db_connection import InfluxDbConnection
from influxdb_connector.influxdb_config import InfluxDBConfig
from influxdb_measure_repository.measure_mapper import MeasureMapper
from influxdb_measure_repository.query_mapping import query_to_flux
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measurement import Measurement, Measurements
from meteo_domain.ports.measure_repository import MeasureRepository


class InfluxDbMeasureRepository(MeasureRepository):
    def __init__(self, config: InfluxDBConfig):
        self.config = config
        self.connection = InfluxDbConnection(config)
        self.mapper = MeasureMapper()

    @override
    async def save_batch(
        self,
        measures: Iterable[Measurement],
        chunk_size: int = 100_000,
    ):
        self.connection.write_batch(
            map(self.mapper.to_model, measures), chunk_size=chunk_size
        )

    @override
    def search(
        self,
        query: MeasureQuery = None,
    ) -> Generator[Measurements, None, None]:
        sensor_ids = [_.uid for _ in query.sources]
        sensor_mapping = dict(zip(sensor_ids, query.sources))

        flux_query = query_to_flux(query=query, bucket=self.config.bucket)
        tables = self.connection.query(flux_query)

        for table in tables:
            measurements = []
            for record in table.records:
                measurements.append(
                    Measurement(
                        sensor=sensor_mapping[record.values.get("sensor_id")],
                        value=record.get_value(),
                        time=record.get_time(),
                    )
                )
            yield Measurements.from_measures(
                sensor=sensor_mapping[table.records[0].values.get("sensor_id")],
                measures=measurements,
            )

    @override
    async def init(self, reset: bool = False):
        buckets_api = self.connection.client.buckets_api()
        try:
            bucket = next(
                (
                    b
                    for b in buckets_api.find_buckets().buckets
                    if b.name == self.config.bucket
                ),
                None,
            )
            if bucket:
                buckets_api.delete_bucket(bucket.id)
        except Exception as e:
            print(f"Warning: Could not delete existing bucket: {e}")

        try:
            org = self.connection.client.organizations_api().find_organizations()[0]
            buckets_api.create_bucket(bucket_name=self.config.bucket, org_id=org.id)
        except Exception as e:
            print(f"Warning: Could not create bucket: {e}")

    def __del__(self):
        if hasattr(self, "influx_connection"):
            self.influx_connection.close()
