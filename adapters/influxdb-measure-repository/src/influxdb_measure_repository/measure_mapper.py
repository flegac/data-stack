from influxdb_client import Point

from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.sensor import Sensor


class MeasureMapper:

    def to_domain(self, point: Point, sensor: Sensor) -> Measurement:
        return Measurement(
            sensor=sensor,
            value=point.get_field("value"),
            time=point.time,
        )

    def to_model(self, measure: Measurement) -> Point:
        return (
            Point(measure.sensor.measure_type.lower())
            .tag("sensor_id", measure.sensor.uid)
            .field("value", measure.value)
            .time(measure.time)
        )
