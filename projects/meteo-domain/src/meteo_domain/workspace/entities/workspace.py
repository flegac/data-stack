from dataclasses import dataclass


@dataclass(frozen=True)
class Workspace:
    uid: str

    @property
    def datafile_bucket(self):
        return f"{self.uid}-datafile-bucket"
