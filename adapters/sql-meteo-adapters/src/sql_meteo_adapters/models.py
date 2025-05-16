from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, func, Enum
from sqlalchemy.orm import declarative_base

from meteo_domain.data_file.entities.datafile_lifecycle import DataFileLifecycle

Base = declarative_base()


class WorkspaceModel(Base):
    __tablename__ = "workspaces"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())


class SensorModel(Base):
    __tablename__ = "sensors"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    measure_type = Column(String, index=True, nullable=False)
    location = Column(Geometry("POINT", srid=4326), index=True, nullable=False)


class DataFileModel(Base):
    __tablename__ = "datafiles"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    source_hash = Column(String, index=True, nullable=False)

    status = Column(Enum(DataFileLifecycle), index=True, nullable=False)
