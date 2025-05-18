import datetime

from meteo_domain.measurement.centroid import Centroid
from meteo_domain.measurement.entities.measurement import TaggedMeasurement
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor


class MeasurementService:

    def randomize(self, centroid: Centroid):
        now = datetime.datetime.now(datetime.UTC)
        return [
            TaggedMeasurement(
                time=now,
                value=centroid.compute_value(pos),
                sensor=Sensor(
                    location=Location(latitude=pos[0], longitude=pos[1]),
                ),
            )
            for pos in centroid.generate_random_points()
        ]
