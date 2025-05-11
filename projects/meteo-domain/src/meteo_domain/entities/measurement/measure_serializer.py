import datetime
import json
from dataclasses import asdict

import pandas as pd

from aa_common.mq.serializer import Serializer
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.measurement.sensor_serializer import SensorSerializer


class MeasureSerializer(Serializer[Measurement, bytes]):
    sensor_serializer = SensorSerializer()

    def serialize(self, message: Measurement) -> bytes:
        measure_dict = asdict(message)
        measure_dict["value"] = (
            float(message.value) if pd.notna(message.value) else None
        )
        measure_dict["time"] = message.time.isoformat()
        measure_dict["sensor"] = self.sensor_serializer.serialize(message.sensor)
        return json.dumps(measure_dict).encode("utf-8")

    def deserialize(self, raw: bytes) -> Measurement:
        raw = json.loads(raw)
        raw["time"] = datetime.datetime.fromisoformat(raw["time"])
        try:
            raw["value"] = float(raw["value"])
        except TypeError:
            raw["value"] = float("nan")
        raw["sensor"] = self.sensor_serializer.deserialize(raw["sensor"])
        return Measurement(**raw)
