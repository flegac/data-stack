from enum import Enum, auto


class TaskStatus(Enum):
    created = auto()  # initial state

    upload_in_progress = auto()
    upload_success = auto()
    upload_error = auto()

    ingestion_pending = auto()
    ingestion_in_progress = auto()
    ingestion_success = auto()
    ingestion_error = auto()
