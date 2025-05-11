from influxdb_client import Point

from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measurement import Measurement


def measure_to_point(measure: Measurement):
    return (
        Point(measure.sensor.measure_type.lower())
        .tag("sensor_id", measure.sensor.uid)
        .field("value", measure.value)
        .time(measure.time)
    )


def query_to_flux(query: MeasureQuery, bucket: str):
    start_time = "-10m"
    end_time = "now()"
    if query.period:
        if query.period.start:
            start_time = query.period.start.isoformat()
        if query.period.end:
            end_time = query.period.end.isoformat()

    flux_query = f"""from(bucket: "{bucket}")
    |> range(start: {start_time}, stop: {end_time})"""

    if query.tags is not None:
        for tag_key, tag_values in query.tags.items():
            if tag_values:
                flux_query += (
                    f"\n    |> filter("
                    f"fn: (r) => contains(value: r.{tag_key}, set: {tag_values}))"
                )

    # sources
    sensor_ids = [_.uid for _ in query.sources]
    sensor_list = ",".join([f'"{_}"' for _ in sensor_ids])
    flux_query += (
        f"\n    |> filter(fn: (r) => contains(value: r.sensor_id, set: [{sensor_list}]))"
        f"\n    |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)"
        f'\n    |> group(columns: ["sensor_id"])'
    )

    return flux_query
