import json
from dataclasses import asdict
from typing import TypeVar, override

from meteo_domain.core.message_queue.serializer import Serializer
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.data_file.entities.datafile_lifecycle import DataFileLifecycle

T = TypeVar("T")
S = TypeVar("S")


class DataFileSerializer(Serializer[DataFile, bytes]):
    @override
    def serialize(self, message: DataFile) -> bytes:
        data_file_dict = asdict(message)
        data_file_dict["status"] = message.status.name
        del data_file_dict["local_path"]
        return json.dumps(data_file_dict).encode("utf-8")

    @override
    def deserialize(self, raw: bytes) -> DataFile:
        raw_dict = json.loads(raw)
        raw_dict["status"] = DataFileLifecycle[raw_dict["status"]]
        return DataFile(**raw_dict)
