import json
from dataclasses import asdict
from datetime import datetime
from typing import TypeVar

from data_file_repository.data_file import DataFile
from data_file_repository.task_status import TaskStatus
from message_queue.serializer import Serializer

T = TypeVar('T')
S = TypeVar('S')


class DataFileSerializer(Serializer[DataFile, bytes]):
    def serialize(self, data_file: DataFile) -> bytes:
        data_file_dict = asdict(data_file)
        data_file_dict['status'] = data_file.status.name
        data_file_dict['creation_date'] = data_file.creation_date.isoformat()
        data_file_dict['last_update_date'] = data_file.last_update_date.isoformat()
        return json.dumps(data_file_dict).encode('utf-8')

    def deserialize(self, raw: bytes) -> DataFile:
        raw_dict = json.loads(raw)
        raw_dict['creation_date'] = datetime.fromisoformat(raw_dict['creation_date'])
        raw_dict['last_update_date'] = datetime.fromisoformat(raw_dict['last_update_date'])
        raw_dict['status'] = TaskStatus[raw_dict['status']]
        return DataFile(**raw_dict)
