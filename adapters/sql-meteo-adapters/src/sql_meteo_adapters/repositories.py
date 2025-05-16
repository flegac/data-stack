from sqlalchemy import func, select

from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.data_file.ports.data_file_repository import DataFileRepository
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.sensor.ports.sensor_repository import SensorRepository
from meteo_domain.workspace.entities.workspace import Workspace
from meteo_domain.workspace.ports.workspace_repository import WorkspaceRepository
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.models import DataFileModel, WorkspaceModel, SensorModel
from sql_meteo_adapters.sensor_mapper import (
    SensorMapper,
    WorkspaceMapper,
    DataFileMapper,
)


class SqlWorkspaceRepository(
    SqlRepository[Workspace, WorkspaceModel],
    WorkspaceRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, WorkspaceMapper)


class SqlDataFileRepository(
    SqlRepository[DataFile, DataFileModel],
    DataFileRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, DataFileMapper)


class SqlSensorRepository(
    SqlRepository[Sensor, SensorModel],
    SensorRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, SensorMapper)

    async def find_in_radius(self, center: Location, radius_km: float) -> list[Sensor]:
        async with self.uow.transaction() as session:
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
