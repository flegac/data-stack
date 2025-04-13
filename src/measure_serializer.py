import datetime
import json
from dataclasses import asdict

import pandas as pd

from brocker_api.serializer import Serializer
from measure_repository import Measure
from measure_repository.model.sensor import MeasureType, Sensor


class MeasureSerializer(Serializer[Measure]):
    def serialize(self, obj: Measure) -> str:
        measure_dict = asdict(obj)
        measure_dict['value'] = float(obj.value) if pd.notna(obj.value) else None
        measure_dict['datetime'] = obj.datetime.isoformat()
        measure_dict['sensor']['type'] = obj.sensor.type.name  # Convert MeasureType to string
        return json.dumps(measure_dict)

    def deserialize(self, data: str) -> Measure:
        raw = json.loads(data)
        raw['datetime'] = datetime.datetime.fromisoformat(raw['datetime'])
        try:
            raw['value'] = float(raw['value'])
        except TypeError:
            raw['value'] = float('nan')
        raw['sensor']['type'] = MeasureType[raw['sensor']['type']]  # Convert string back to MeasureType
        raw['sensor'] = Sensor(**raw['sensor'])
        return Measure(**raw)
