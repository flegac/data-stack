from influxdb_client import Point

from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measures.measurement import Measurement


def measure_to_point(measure: Measurement):
    return (
        Point(measure.sensor.type.lower())
        .tag("sensor_id", measure.sensor.id)
        .field("value", measure.value)
    )


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
