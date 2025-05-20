from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.datafile_lifecycle import (
    DataFileLifecycle,
)
from sql_connector.model_mapper import ModelMapper
from sql_connector.sql_connection import BaseModel, SqlConnection
from sql_connector.sql_repository import SqlRepository
from sqlalchemy import Column, Date, Enum, String, func

from unit_of_work_sql.patches.location_patch import LocationPatch


class DataFileModel(BaseModel):
    __tablename__ = "datafiles"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    source_hash = Column(String, index=True, nullable=False)

    status = Column(Enum(DataFileLifecycle), index=True, nullable=False)


DataFileMapper = ModelMapper(DataFile, DataFileModel, patches=[LocationPatch()])


class SqlDataFileRepository(SqlRepository[DataFile, DataFileModel]):
    def __init__(self, connection: SqlConnection):
        super().__init__(connection, DataFileMapper)
