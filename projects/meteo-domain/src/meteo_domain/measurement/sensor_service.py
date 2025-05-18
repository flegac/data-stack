import random

from meteo_domain.measurement.centroid import Centroid
from meteo_domain.measurement.entities.measurement import TaggedMeasurement
from meteo_domain.measurement.entities.period import Period
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor


class SensorService:
    def fake_measurements(self, sensor: Sensor, period: Period, size: int):
        value = random.normalvariate(10.0, 25.0)
        for time in period.split(size):
            value += random.normalvariate(0.0, 1.0)
            yield TaggedMeasurement(
                sensor=sensor,
                time=time,
                value=value,
            )

    def fake_sensors(self, centroid: Centroid):
        for pos in centroid.generate_random_points():
            yield Sensor(
                location=Location(longitude=pos[0], latitude=pos[1]),
            )

    def randomize(self, centroid: Centroid, period: Period, steps: int):
        sensors = self.fake_sensors(centroid)

        for sensor in sensors:
            yield from self.fake_measurements(sensor, period, steps)
