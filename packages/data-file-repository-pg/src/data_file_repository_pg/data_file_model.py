from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import declarative_base

from data_file_repository.task_status import TaskStatus

Base = declarative_base()


class DataFileModel(Base):
    __tablename__ = 'datafile'
    key = Column(String, primary_key=True)
    source_hash = Column(String, nullable=False)
    source_uri = Column(String, nullable=False)
    status = Column(SqlEnum(TaskStatus), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update_date = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
