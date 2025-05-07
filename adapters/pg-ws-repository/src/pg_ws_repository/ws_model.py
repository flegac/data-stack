from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WorkspaceModel(Base):
    __tablename__ = "workspace"
    workspace_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update_date = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
