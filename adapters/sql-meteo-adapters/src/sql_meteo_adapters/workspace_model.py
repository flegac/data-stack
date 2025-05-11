from datetime import datetime

from sqlmodel import Field, SQLModel


class WorkspaceModel(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    creation_date: datetime = Field(default_factory=datetime.now)
    last_update_date: datetime = Field(default_factory=datetime.now)

    name: str = Field(nullable=False)
