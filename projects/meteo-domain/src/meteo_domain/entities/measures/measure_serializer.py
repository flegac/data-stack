import datetime
import json
from dataclasses import asdict

import pandas as pd
from message_queue.serializer import Serializer

from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.entities.measures.sensor import Sensor


class MeasureSerializer(Serializer[Measurement, bytes]):
    def serialize(self, message: Measurement) -> bytes:
        measure_dict = asdict(message)
        measure_dict["value"] = (
            float(message.value) if pd.notna(message.value) else None
        )
        measure_dict["datetime"] = message.datetime.isoformat()
        return json.dumps(measure_dict).encode("utf-8")

    def deserialize(self, raw: bytes) -> Measurement:
        raw = json.loads(raw)
        raw["datetime"] = datetime.datetime.fromisoformat(raw["datetime"])
        try:
            raw["value"] = float(raw["value"])
        except TypeError:
            raw["value"] = float("nan")
        raw["sensor"] = Sensor(**raw["sensor"])
        return Measurement(**raw)
