from sqlalchemy import Column, String, Date, func, Enum

from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.data_file.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.ports.data_file_repository import DataFileRepository
from sql_connector.model_mapper import ModelMapper
from sql_connector.patches.location_patch import LocationPatch
from sql_connector.sql_connection import BaseModel
from sql_connector.sql_repository import SqlRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork


class DataFileModel(BaseModel):
    __tablename__ = "datafiles"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    source_hash = Column(String, index=True, nullable=False)

    status = Column(Enum(DataFileLifecycle), index=True, nullable=False)


DataFileMapper = ModelMapper(DataFile, DataFileModel, patches=[LocationPatch()])


class SqlDataFileRepository(
    SqlRepository[DataFile, DataFileModel],
    DataFileRepository,
):
    def __init__(self, uow: SqlUnitOfWork):
        super().__init__(uow, DataFileMapper)
