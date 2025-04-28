from enum import Enum, auto


class TaskStatus(Enum):
    pending = auto()
    in_progress = auto()
    success = auto()
    error = auto()
