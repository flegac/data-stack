import datetime
from dataclasses import dataclass

import numpy as np

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.telemetry.geo_sensor_series import GeoSensorSeries
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry


@dataclass(frozen=True)
class RegionSeries:
    series: list[GeoSensorSeries]

    def iter_timeline(self):
        times = [_.time for _ in self.series[0].measures]
        for idx, _time in enumerate(times):
            yield [TaggedTelemetry.tag(_.sensor, _.measures[idx]) for _ in self.series]


@dataclass(frozen=True)
class InstantPicture:
    time: datetime.datetime
    sensors: list[GeoSensor]
    values: np.ndarray

    def iter(self):
        for sensor, value in zip(self.sensors, self.values, strict=False):
            yield TaggedTelemetry(
                sensor=sensor,
                time=self.time,
                value=value,
            )
