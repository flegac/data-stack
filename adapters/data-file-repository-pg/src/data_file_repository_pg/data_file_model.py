from datetime import datetime

from meteo_measures.domain.entities.datafile_lifecycle import DataFileLifecycle
from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DataFileModel(Base):
    __tablename__ = "datafile"
    key = Column(String, primary_key=True)
    source_hash = Column(String, nullable=False)
    source_uri = Column(String, nullable=False)
    status = Column(SqlEnum(DataFileLifecycle), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update_date = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
