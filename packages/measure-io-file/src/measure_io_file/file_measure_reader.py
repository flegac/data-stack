from typing import override, Generator, Any

import pandas as pd
import xarray as xr

from measure_io.measure import MeasureSeries
from measure_io.measure_reader import MeasureReader
from measure_io.sensor import Sensor, MeasureType, Location
from measure_io_file.file_config import FileConfig


class FileMeasureReader(MeasureReader):

    def __init__(self, config: FileConfig):
        super().__init__()
        self.config = config
        self.show_config()

    def show_config(self):
        print(self.config.raw)

    @override
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        dataset = self.config.raw
        latitudes = dataset['latitude']
        longitudes = dataset['longitude']
        print(len(latitudes), len(longitudes))

        for lat_idx in range(len(latitudes)):
            for lon_idx in range(len(longitudes)):
                for variable in self.config.variables:
                    temperatures = MeasureSeries(
                        sensor=Sensor(
                            id="cds",
                            type=MeasureType.TEMPERATURE,
                            location=Location(
                                latitude=float(latitudes.values[lat_idx]),
                                longitude=float(longitudes.values[lon_idx])
                            ),
                        ),
                        measures=self._extract_time_series(dataset, variable, lat_idx, lon_idx)
                    )
                    yield temperatures

    @staticmethod
    def _extract_time_series(dataset: xr.Dataset, variable_name: str, lat_idx: int, lon_idx: int) -> pd.DataFrame:
        # Sélectionner les données pour les indices de latitude et de longitude spécifiés
        data_array = dataset[variable_name].isel(latitude=lat_idx, longitude=lon_idx)

        # Créer les valeurs de datetime
        datetime_values = dataset['time'].values

        # Aplatir les valeurs de données
        data_values = data_array.values.flatten()

        # Créer un DataFrame pandas
        df = pd.DataFrame({
            'datetime': datetime_values,
            'value': data_values
        })

        return df
