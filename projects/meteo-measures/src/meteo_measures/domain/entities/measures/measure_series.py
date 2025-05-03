from dataclasses import dataclass

import pandas as pd

from meteo_measures.domain.entities.measures.measurement import Measurement
from meteo_measures.domain.entities.measures.sensor import Sensor


@dataclass
class MeasureSeries:
    sensor: Sensor
    measures: pd.DataFrame  # { 'datetime': datetime, 'value': float }

    @staticmethod
    def from_measures(sensor: Sensor, measures: list[Measurement]):
        return MeasureSeries(
            sensor=sensor,
            measures=pd.DataFrame(
                data={
                    "datetime": [_.datetime for _ in measures],
                    "value": [_.value for _ in measures],
                }
            ),
        )

    def __iter__(self):
        for _, row in self.measures.iterrows():
            yield Measurement(
                sensor=self.sensor, datetime=row["datetime"], value=row["value"]
            )
