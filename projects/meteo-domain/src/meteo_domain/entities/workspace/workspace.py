from dataclasses import dataclass, field

WorkspaceId = str


@dataclass
class Workspace:
    """
    A workspace serves as a container for meteo data.
    """

    id: WorkspaceId
    name: str

    inclusion_tags: list[str]
    exclusion_tags: list[str]

    @property
    def datafile_bucket(self):
        return f"{self.id}-datafile-bucket"


@dataclass(kw_only=True)
class WorkObject:
    workspace_id: WorkspaceId | None = None
    tags: list[str] = field(default_factory=list)
