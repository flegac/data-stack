from dataclasses import dataclass

from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry


@dataclass
class TaggedTSeries:
    measures: list[TaggedTelemetry]

    def iter_tagged(self):
        yield from self.measures

    def iter_untagged(self):
        for _ in self.measures:
            yield _.untag()

    def __iter__(self):
        yield from self.iter_tagged()
