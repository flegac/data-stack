import datetime
import random

from easy_kit.timing import time_func

from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.location.location import Location
from meteo_domain.geo_sensor.entities.location.locations import Locations
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry
from meteo_domain.geo_sensor.entities.times.period import Period
from meteo_domain.geo_sensor.generator import Generator


class SensorService:
    def retrieve_locations(self, sensors: list[GeoSensor]) -> Locations:
        pass

    @time_func
    def fake_measurements(self, sensor: GeoSensor, period: Period, size: int):
        value = random.normalvariate(0.0, 1.0)

        for time in period.split(size):
            value += random.normalvariate(0.0, 0.5)
            yield TaggedTelemetry(
                sensor=sensor,
                time=time,
                value=value,
            )

    def fake_measurements2(self, source: Generator, n: int):
        now = datetime.datetime.now(datetime.UTC)

        for pos in source.geo.normal(source.center, n):
            yield TaggedTelemetry(
                time=now,
                value=source.value.compute_value(pos),
                sensor=GeoSensor(
                    location=Location.from_raw(pos),
                ),
            )
