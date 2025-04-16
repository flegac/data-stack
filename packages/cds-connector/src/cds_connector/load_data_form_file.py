import math
from pathlib import Path

import pandas as pd
import xarray as xr

from measure_feature import MeasureSeries
from measure_feature.model.sensor import Sensor, MeasureType, Location


def extract_time_series(dataset: xr.Dataset, variable_name: str, lat_idx: int, lon_idx: int) -> pd.DataFrame:
    # Sélectionner les données pour les indices de latitude et de longitude spécifiés
    data_array = dataset[variable_name].isel(latitude=lat_idx, longitude=lon_idx)

    # Créer les valeurs de datetime
    datetime_values = dataset['valid_time'].values

    # Aplatir les valeurs de données
    data_values = data_array.values.flatten()

    # Créer un DataFrame pandas
    df = pd.DataFrame({
        'datetime': datetime_values,
        'value': data_values
    })

    return df


def main():
    path = Path.home() / 'Documents' / 'Data' / 'Datasets'
    filepath = path / 'CDS-2025-01.grib'
    filepath = path / 'CDS-1983-10-22.nc'
    filepath = path / 'CDS-1983-10.nc'


    ds_xarray = xr.open_dataset(filepath)
    latitudes = ds_xarray['latitude']
    longitudes = ds_xarray['longitude']
    print(ds_xarray)
    print(len(latitudes), len(longitudes))

    temperatures = MeasureSeries(
        sensor=Sensor(
            id="cds",
            type=MeasureType.TEMPERATURE,
            location=Location(
                latitude=float(ds_xarray['latitude'].values[700]),
                longitude=float(ds_xarray['longitude'].values[1800])
            ),
        ),
        measures=extract_time_series(ds_xarray, 't2m', 50, 50)
    )
    print(temperatures.sensor, temperatures.measures.head())


    # for lat_idx in range(len(ds_xarray['latitude'])):
    #     for lon_idx in range(len(ds_xarray['longitude'])):
    #         temperatures = MeasureSeries(
    #             sensor=Sensor(
    #                 id="cds",
    #                 type=MeasureType.TEMPERATURE,
    #                 location=Location(
    #                     latitude=float(ds_xarray['latitude'].values[lat_idx]),
    #                     longitude=float(ds_xarray['longitude'].values[lon_idx])
    #                 ),
    #             ),
    #             measures=extract_time_series(ds_xarray, 't2m', lat_idx, lon_idx)
    #         )
    #         max_value = temperatures.measures['value'].max()
    #
    #         if not math.isnan(max_value):
    #             print(temperatures.sensor, max_value)
    #
    #         print(temperatures.sensor, temperatures.measures.head())

if __name__ == '__main__':
    main()
