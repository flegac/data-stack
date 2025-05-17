from dataclasses import dataclass

from meteo_domain.measurement.entities.sensor.sensor import Sensor
from meteo_domain.measurement.entities.measurement import (
    Measurement,
    TaggedMeasurement,
)


@dataclass
class TSeries:
    sensor: Sensor
    measures: list[Measurement]

    @staticmethod
    def from_measures(sensor: Sensor, measures: list[Measurement]):
        return TSeries(
            sensor=sensor,
            measures=measures,
        )

    def iter_tagged(self):
        for _ in self.measures:
            yield _.tag(self.sensor)

    def iter_untagged(self):
        yield from self.measures

    def __iter__(self):
        yield from self.iter_tagged()

    def __repr__(self):
        measures = "\n".join([f"{_.time} {_.value}" for _ in self.measures[:5]])
        return f"{self.sensor}\n{measures}"


@dataclass
class TaggedTSeries:
    measures: list[TaggedMeasurement]

    def iter_tagged(self):
        yield from self.measures

    def iter_untagged(self):
        for _ in self.measures:
            yield _.untag()

    def __iter__(self):
        yield from self.iter_tagged()
