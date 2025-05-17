from influxdb_client import Point

from meteo_domain.measurement.entities.sensor.sensor import Sensor
from meteo_domain.measurement.entities.measurement import (
    TaggedMeasurement,
)


class MeasureMapper:
    def to_domain(self, point: Point, sensor: Sensor) -> TaggedMeasurement:
        return TaggedMeasurement(
            value=point.get_field("value"),
            time=point.time,
            sensor=sensor,
        )

    def to_model(self, measure: TaggedMeasurement) -> Point:
        return (
            Point(measure.sensor.measure_type.lower())
            .tag("sensor_id", measure.sensor.uid)
            .field("value", measure.value)
            .time(measure.time)
        )
