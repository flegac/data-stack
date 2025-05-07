import json
from dataclasses import asdict
from datetime import datetime
from typing import TypeVar, override

from aa_common.mq.serializer import Serializer
from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle

T = TypeVar("T")
S = TypeVar("S")


class DataFileSerializer(Serializer[DataFile, bytes]):
    @override
    def serialize(self, message: DataFile) -> bytes:
        data_file_dict = asdict(message)
        data_file_dict["status"] = message.status.name
        data_file_dict["creation_date"] = message.creation_date.isoformat()
        data_file_dict["last_update_date"] = message.last_update_date.isoformat()
        del data_file_dict["local_path"]
        return json.dumps(data_file_dict).encode("utf-8")

    @override
    def deserialize(self, raw: bytes) -> DataFile:
        raw_dict = json.loads(raw)
        raw_dict["creation_date"] = datetime.fromisoformat(raw_dict["creation_date"])
        raw_dict["last_update_date"] = datetime.fromisoformat(
            raw_dict["last_update_date"]
        )
        raw_dict["status"] = DataFileLifecycle[raw_dict["status"]]
        return DataFile(**raw_dict)
