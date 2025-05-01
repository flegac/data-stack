from dataclasses import dataclass
from datetime import datetime


@dataclass
class Period:
    start: datetime | None = None
    end: datetime | None = None
