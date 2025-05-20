from dataclasses import dataclass

import numpy as np

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry
from meteo_domain.geo_sensor.entities.times.times import Times


@dataclass(frozen=True)
class Telemetries:
    sensors: list[GeoSensor]
    times: Times
    values: np.ndarray

    @staticmethod
    def merge(items: list["Telemetries"]):
        sensors = []
        for _ in items:
            sensors.extend(_.sensors)

        times = Times.merge([_.times for _ in items])
        values = np.concatenate([_.values for _ in items], axis=0)
        return Telemetries(
            sensors=sensors,
            times=times,
            values=values,
        )

    @property
    def size(self):
        return self.times.size

    def iter(self):
        for _ in range(self.size):
            yield TaggedTelemetry(
                sensor=self.sensors[_],
                time=self.times.read(_),
                value=float(self.values[_]),
            )
