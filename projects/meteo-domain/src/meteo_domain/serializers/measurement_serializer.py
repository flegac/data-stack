import datetime
import json
from dataclasses import asdict

import pandas as pd

from meteo_domain.core.message_queue.serializer import Serializer
from meteo_domain.geo_sensor.entities.telemetry.telemetry import Telemetry
from meteo_domain.serializers.sensor_serializer import SensorSerializer


class MeasurementSerializer(Serializer[Telemetry, bytes]):
    sensor_serializer = SensorSerializer()

    def serialize(self, message: Telemetry) -> bytes:
        measure_dict = asdict(message)
        measure_dict["value"] = (
            float(message.value) if pd.notna(message.value) else None
        )
        measure_dict["times"] = message.time.isoformat()
        return json.dumps(measure_dict).encode("utf-8")

    def deserialize(self, raw: bytes) -> Telemetry:
        raw = json.loads(raw)
        raw["time"] = datetime.datetime.fromisoformat(raw["time"])
        try:
            raw["value"] = float(raw["value"])
        except TypeError:
            raw["value"] = float("nan")
        return Telemetry(**raw)
