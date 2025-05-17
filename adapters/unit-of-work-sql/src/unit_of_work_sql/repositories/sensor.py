from geoalchemy2 import Geometry
from sqlalchemy import func, select, Column, String, Date

from meteo_domain.datafile_ingestion.ports.uow.geo_repository import (
    GeoRepository,
)
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_connection import BaseModel, SqlConnection
from sql_connector.sql_repository import SqlRepository
from unit_of_work_sql.patches.location_patch import LocationPatch


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
    GeoRepository[Sensor],
):
    def __init__(self, connection: SqlConnection):
        super().__init__(connection, SensorMapper)

    async def find_in_radius(self, center: Location, radius_km: float) -> list[Sensor]:
        point = func.ST_Transform(
            func.ST_SetSRID(func.ST_MakePoint(center.longitude, center.latitude), 4326),
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
        result = await self.session.execute(stmt)
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
