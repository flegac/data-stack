import datetime
import json
from dataclasses import asdict

import pandas as pd

from broker_api.serializer import Serializer
from measure_repository import Measure
from measure_repository.model.sensor import MeasureType, Sensor


class MeasureSerializer(Serializer[Measure, str]):
    def serialize(self, message: Measure) -> str:
        measure_dict = asdict(message)
        measure_dict['value'] = float(message.value) if pd.notna(message.value) else None
        measure_dict['datetime'] = message.datetime.isoformat()
        measure_dict['sensor']['type'] = message.sensor.type.name  # Convert MeasureType to string
        return json.dumps(measure_dict)

    def deserialize(self, raw: str) -> Measure:
        raw = json.loads(raw)
        raw['datetime'] = datetime.datetime.fromisoformat(raw['datetime'])
        try:
            raw['value'] = float(raw['value'])
        except TypeError:
            raw['value'] = float('nan')
        raw['sensor']['type'] = MeasureType[raw['sensor']['type']]  # Convert string back to MeasureType
        raw['sensor'] = Sensor(**raw['sensor'])
        return Measure(**raw)
