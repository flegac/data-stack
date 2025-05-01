import datetime
import json
from dataclasses import asdict

import pandas as pd

from message_queue.serializer import Serializer
from meteo_measures.entities.measures.measure import Measure
from meteo_measures.entities.measures.measure_type import MeasureType
from meteo_measures.entities.measures.sensor import Sensor


class MeasureSerializer(Serializer[Measure, bytes]):
    def serialize(self, message: Measure) -> bytes:
        measure_dict = asdict(message)
        measure_dict['value'] = float(message.value) if pd.notna(message.value) else None
        measure_dict['datetime'] = message.datetime.isoformat()
        measure_dict['sensor']['type'] = message.sensor.type.name  # Convert MeasureType to string
        return json.dumps(measure_dict).encode('utf-8')

    def deserialize(self, raw: bytes) -> Measure:
        raw = json.loads(raw)
        raw['datetime'] = datetime.datetime.fromisoformat(raw['datetime'])
        try:
            raw['value'] = float(raw['value'])
        except TypeError:
            raw['value'] = float('nan')
        raw['sensor']['type'] = MeasureType[raw['sensor']['type']]  # Convert string back to MeasureType
        raw['sensor'] = Sensor(**raw['sensor'])
        return Measure(**raw)
