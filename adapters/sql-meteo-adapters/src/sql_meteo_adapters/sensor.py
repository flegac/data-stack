from geoalchemy2 import Geometry
from sqlalchemy import func, select, Column, String, Date

from meteo_domain.ports.sensor_repository import SensorRepository
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from sql_connector.model_mapper import ModelMapper
from sql_connector.patches.location_patch import LocationPatch
from sql_connector.sql_connection import BaseModel
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


class SensorModel(BaseModel):
    __tablename__ = "sensors"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    measure_type = Column(String, index=True, nullable=False)
    location = Column(Geometry("POINT", srid=4326), index=True, nullable=False)


SensorMapper = ModelMapper(Sensor, SensorModel, patches=[LocationPatch()])


class SqlSensorRepository(
    SqlRepository[Sensor, SensorModel],
    SensorRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, SensorMapper)

    async def find_in_radius(self, center: Location, radius_km: float) -> list[Sensor]:
        async with self.uow.transaction():
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
            result = await self.uow.session.execute(stmt)
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
