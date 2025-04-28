from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from measure_io.sensor import Sensor


@dataclass
class Measure:
    datetime: datetime
    value: float
    sensor: Sensor | None = None


@dataclass
class MeasureSeries:
    sensor: Sensor
    measures: pd.DataFrame  # { 'datetime': datetime, 'value': float }

    @staticmethod
    def from_measures(sensor: Sensor, measures: list[Measure]):
        return MeasureSeries(
            sensor=sensor,
            measures=pd.DataFrame(data={
                'datetime': [_.datetime for _ in measures],
                'value': [_.value for _ in measures]
            })
        )

    def __iter__(self):
        for index, row in self.measures.iterrows():
            yield Measure(sensor=self.sensor, datetime=row['datetime'], value=row['value'])
