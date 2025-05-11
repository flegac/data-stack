from sqlalchemy import func, select

from meteo_domain.entities.geo_spatial.location import Location
from meteo_domain.entities.sensor import Sensor
from meteo_domain.ports.sensor_repository import SensorRepository
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository
from sql_meteo_adapters.sensor_mapper import SensorMapper
from sql_meteo_adapters.sensor_model import SensorModel


class SqlSensorRepository(
    SqlRepository[Sensor, SensorModel],
    SensorRepository,
):

    def __init__(self, connection: SqlConnection):
        super().__init__(connection, SensorMapper())

    async def find_in_radius(self, center: Location, radius_km: float) -> list[Sensor]:
        async with self.connection.transaction() as session:
            point = func.ST_Transform(
                func.ST_SetSRID(
                    func.ST_MakePoint(center.longitude, center.latitude), 4326
                ),
                3857,
            )
            stmt = select(
                SensorModel.uid,
                func.ST_AsText(SensorModel.location).label("location_wkt"),
            ).where(
                func.ST_DWithin(
                    func.ST_Transform(SensorModel.location, 3857),
                    point,
                    radius_km * 1_000,
                    use_spheroid=True,
                )
            )
            result = await session.execute(stmt)
            return [
                Sensor(
                    uid=row.uid,
                    measure_type="temperature",
                    location=Location(
                        longitude=float(row.location_wkt.strip("POINT()").split()[0]),
                        latitude=float(row.location_wkt.strip("POINT()").split()[1]),
                    ),
                )
                for row in result
            ]
