from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import declarative_base

from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle

Base = declarative_base()


# pylint: disable=too-few-public-methods
class DataFileModel(Base):
    __tablename__ = "datafile"
    uid = Column(String, primary_key=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update_date = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    workspace_id = Column(String, nullable=True)
    source_hash = Column(String, nullable=False)
    status = Column(SqlEnum(DataFileLifecycle), nullable=False)
