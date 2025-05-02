from enum import Enum, auto


class DataFileLifecycle(Enum):
    created = auto()

    upload_in_progress = auto()
    upload_completed = auto()
    upload_failed = auto()

    ingestion_in_progress = auto()
    ingestion_completed = auto()
    ingestion_failed = auto()

    completed = auto()
