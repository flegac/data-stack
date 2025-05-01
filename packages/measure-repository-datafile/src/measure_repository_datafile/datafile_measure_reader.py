import time
from typing import override, Generator, Any

import pandas as pd
import xarray as xr
from loguru import logger

from data_file_repository.data_file import DataFile
from measure_repository.model.location import Location
from measure_repository.model.measure_series import MeasureSeries
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.sensor import Sensor
from measure_repository.stream.measure_reader import MeasureReader


class DataFileMeasureReader(MeasureReader):

    def __init__(self, datafile: DataFile):
        super().__init__()
        self.datafile = datafile
        self.show_config()

    def show_config(self):
        logger.debug(self.datafile.raw)
        time.sleep(.1)

    @override
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        dataset = self.datafile.raw
        latitudes = dataset['latitude']
        longitudes = dataset['longitude']
        print(len(latitudes), len(longitudes))

        variables = [
            _
            for _ in self.datafile.variables
            if _ not in ['latitude', 'longitude']
        ]

        for variable in variables:
            try:
                for lat_idx in range(len(latitudes)):
                    for lon_idx in range(len(longitudes)):
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
            except Exception as e:
                logger.warning(f'Could not handle variable=[{variable}] : {e}')

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
