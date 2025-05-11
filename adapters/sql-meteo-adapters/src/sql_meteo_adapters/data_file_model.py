from datetime import datetime

from sqlmodel import SQLModel, Field

from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle


class DataFileModel(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    creation_date: datetime = Field(default_factory=datetime.now)
    last_update_date: datetime = Field(default_factory=datetime.now)
    workspace_id: str | None = Field(index=True, default=None)

    source_hash: str = Field(index=True, nullable=False)
    status: DataFileLifecycle = Field(index=True, nullable=False)
