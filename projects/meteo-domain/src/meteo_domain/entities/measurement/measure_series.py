from dataclasses import dataclass

import pandas as pd

from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.sensor import Sensor


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
                    "time": [_.time for _ in measures],
                    "value": [_.value for _ in measures],
                }
            ),
        )

    def __iter__(self):
        for _, row in self.measures.iterrows():
            yield Measurement(sensor=self.sensor, time=row["time"], value=row["value"])

    def __repr__(self):
        return f"{self.sensor}\n{self.measures.head()}"
