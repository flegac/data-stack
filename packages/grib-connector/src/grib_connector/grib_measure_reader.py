from typing import override, Generator, Any

import pandas as pd
import xarray as xr

from grib_connector.grib_config import GribConfig
from measure_feature import MeasureSeries, MeasureQuery
from measure_feature.api.measure_reader import MeasureReader
from measure_feature.model.sensor import Sensor, MeasureType, Location


class GribMeasureReader(MeasureReader):

    def __init__(self, config: GribConfig):
        super().__init__()
        self.config = config
        self.raw = xr.open_dataset(self.config.path)
        print(self.raw)

    @override
    def read_all(self) -> Generator[MeasureSeries, Any, None]:
        ds_xarray = self.raw
        latitudes = ds_xarray['latitude']
        longitudes = ds_xarray['longitude']
        print(ds_xarray)
        print(len(latitudes), len(longitudes))

        for lat_idx in range(len(ds_xarray['latitude'])):
            for lon_idx in range(len(ds_xarray['longitude'])):
                temperatures = MeasureSeries(
                    sensor=Sensor(
                        id="cds",
                        type=MeasureType.TEMPERATURE,
                        location=Location(
                            latitude=float(ds_xarray['latitude'].values[lat_idx]),
                            longitude=float(ds_xarray['longitude'].values[lon_idx])
                        ),
                    ),
                    measures=self._extract_time_series(ds_xarray, 'precip', lat_idx, lon_idx)
                )
                yield temperatures

    @override
    def search(self, query: MeasureQuery) -> MeasureSeries:
        raise NotImplementedError

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
