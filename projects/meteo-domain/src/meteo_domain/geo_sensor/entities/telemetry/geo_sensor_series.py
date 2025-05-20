from dataclasses import dataclass

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry
from meteo_domain.geo_sensor.entities.telemetry.telemetry import (
    Telemetry,
)


@dataclass
class GeoSensorSeries:
    sensor: GeoSensor
    measures: list[Telemetry]

    @staticmethod
    def from_measures(sensor: GeoSensor, measures: list[Telemetry]):
        return GeoSensorSeries(
            sensor=sensor,
            measures=measures,
        )

    def iter_tagged(self):
        for _ in self.measures:
            yield TaggedTelemetry.tag(self.sensor, _)

    def iter_untagged(self):
        yield from self.measures

    def __iter__(self):
        yield from self.iter_tagged()

    def __repr__(self):
        measures = "\n".join([f"{_.time} {_.value}" for _ in self.measures[:5]])
        return f"{self.sensor}\n{measures}"


