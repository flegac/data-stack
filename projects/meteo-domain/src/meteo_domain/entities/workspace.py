from dataclasses import dataclass, field
from datetime import datetime

from aa_common.repo.repository import UID

WorkspaceId = str


@dataclass(kw_only=True)
class Updatable:
    uid: str
    creation_date: datetime = field(default_factory=datetime.now)
    last_update_date: datetime = field(default_factory=datetime.now)


@dataclass(kw_only=True)
class Workspace(Updatable):
    """
    A workspace serves as a container for meteo data.
    """

    name: str
    inclusion_tags: list[str] = field(default_factory=list)
    exclusion_tags: list[str] = field(default_factory=list)

    @staticmethod
    def from_name(name: str):
        return Workspace(uid=name, name=name)

    @property
    def datafile_bucket(self):
        return f"{self.uid}-datafile-bucket"


@dataclass(kw_only=True)
class WorkObject(Updatable):
    workspace_id: UID | None = None
    # tags: list[str] = field(default_factory=list)
