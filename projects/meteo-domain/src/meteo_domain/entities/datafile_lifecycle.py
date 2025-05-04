from enum import Enum, auto


# pylint: disable=invalid-name
class DataFileLifecycle(Enum):
    created = auto()

    upload_in_progress = auto()
    upload_completed = auto()
    upload_failed = auto()

    ingestion_in_progress = auto()
    ingestion_completed = auto()
    ingestion_failed = auto()

    completed = auto()


# pylint: enable=invalid-name
