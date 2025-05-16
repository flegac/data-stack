from typing import override

from geoalchemy2.shape import from_shape
from shapely import Point

from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from sql_connector.model_mapping import ModelDomainMapper
from sql_meteo_adapters.sensor_model import SensorModel


class SensorMapper(ModelDomainMapper[Sensor, SensorModel]):
    def __init__(self):
        self.entity = Sensor
        self.model = SensorModel

    @override
    def primary_key(self) -> str:
        return "uid"

    @override
    def to_domain(self, model: SensorModel) -> Sensor:
        point_wkt = str(model.location)  # Format WKT: 'POINT(lon lat)'
        lon, lat = point_wkt.strip("POINT()").split()

        return Sensor(
            uid=model.uid,
            measure_type=model.type,
            location=Location(
                latitude=float(lat),
                longitude=float(lon),
            ),
        )

    @override
    def to_model(self, sensor: Sensor) -> SensorModel:
        point = Point(sensor.location.longitude, sensor.location.latitude)
        geom = from_shape(point, srid=4326)

        # lat = sensor.location.latitude
        # lon = sensor.location.longitude
        # location = f"SRID=4326;POINT({lon} {lat})"

        return SensorModel(
            uid=sensor.uid,
            type=sensor.measure_type,
            workspace_id=sensor.workspace_id,
            location=geom,
        )
