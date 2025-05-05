from collections import defaultdict
from collections.abc import Generator, Iterable
from typing import Any, override

from influxdb_connector.influx_db_connection import InfluxDbConnection
from influxdb_connector.influxdb_config import InfluxDBConfig
from measure_repository_influxdb.query_mapping import query_to_flux, measure_to_point
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.entities.measures.sensor import Sensor, SensorId
from meteo_domain.ports.measure_repository import MeasureRepository


class InfluxDbMeasureRepository(MeasureRepository):
    def __init__(self, config: InfluxDBConfig):
        self.config = config
        self.connection = InfluxDbConnection(config)

    @override
    async def save(self, measure: Measurement):
        record = measure_to_point(measure)
        self.connection.write(record=record)

    @override
    async def save_batch(self, measures: Iterable[Measurement]):
        records = [measure_to_point(_) for _ in measures]
        self.connection.write(record=records)

    @override
    def search(self, query: MeasureQuery = None) -> Generator[MeasureSeries, Any, None]:
        flux_query = query_to_flux(query=query, bucket=self.config.bucket)
        tables = self.connection.query(flux_query)
        sensors: dict[tuple[SensorId, str], Sensor] = {}
        measurements: dict[tuple[SensorId, str], list[Measurement]] = defaultdict(list)

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
                measurements[key].append(
                    Measurement(
                        datetime=record.values["_time"],
                        value=record.values["_value"],
                    )
                )

        for key, measures in measurements.items():
            yield MeasureSeries.from_measures(sensors[key], measures)
