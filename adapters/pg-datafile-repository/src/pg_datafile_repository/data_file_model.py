from datetime import datetime

from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from sqlalchemy import Column, DateTime, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# pylint: disable=too-few-public-methods
class DataFileModel(Base):
    __tablename__ = "datafile"
    data_id = Column(String, primary_key=True)
    workspace_id = Column(String, nullable=True)
    source_hash = Column(String, nullable=False)
    source_uri = Column(String, nullable=False)
    status = Column(SqlEnum(DataFileLifecycle), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update_date = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
