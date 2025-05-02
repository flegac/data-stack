import random
from datetime import datetime
from pathlib import Path

import pandas as pd
import xarray as xr
from meteo_measures.domain.entities.data_file import DataFile
from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.measurement import Measurement
from meteo_measures.domain.entities.measures.sensor import Sensor


def measure_series_to_xarray(measure_series: list[Measurement]) -> xr.Dataset:
    # Convert the list of Measurement objects to a pandas DataFrame
    data = {
        "time": [measure.datetime for measure in measure_series],
        "value": [measure.value for measure in measure_series],
        "latitude": [measure.sensor.location.latitude for measure in measure_series],
        "longitude": [measure.sensor.location.longitude for measure in measure_series],
    }
    df = pd.DataFrame(data)

    # Pivot the DataFrame to create a 3D array
    pivot_df = df.pivot_table(
        index="time", columns=["latitude", "longitude"], values="value"
    )

    # Create the xarray Dataset
    coords = {
        "time": pivot_df.index,
        "latitude": pivot_df.columns.get_level_values("latitude").unique(),
        "longitude": pivot_df.columns.get_level_values("longitude").unique(),
    }
    data_vars = {
        "value": (
            ["time", "latitude", "longitude"],
            pivot_df.values.reshape(len(pivot_df.index), -1).reshape(
                (
                    len(coords["time"]),
                    len(coords["latitude"]),
                    len(coords["longitude"]),
                )
            ),
        ),
    }
    attrs = {
        "sensor_id": measure_series[0].sensor.id if measure_series else None,
        "sensor_type": measure_series[0].sensor.type if measure_series else None,
        "sensor_location": (
            str(measure_series[0].sensor.location) if measure_series else None
        ),
    }
    dataset = xr.Dataset(
        data_vars,
        coords=coords,
        attrs=attrs,
    )
    return dataset


# Exemple d'utilisation
if __name__ == "__main__":
    measures = [
        Measurement(
            datetime=time_,
            value=random.random(),
            sensor=Sensor(
                id="test",
                type="temperature",
                location=Location(
                    latitude=latitude,
                    longitude=longitude,
                ),
            ),
        )
        for latitude in range(5)
        for longitude in range(10)
        for time_ in [datetime(2023, 10, 1, hour, 0) for hour in range(24)]
    ]

    path = Path.cwd() / "measure_series.grib"

    dataset = measure_series_to_xarray(measures)
    dataset.to_netcdf(
        path,
        # engine="cfgrib",
    )

    xxx = DataFile.from_file(path)
    print(xxx.raw)

    # for _ in DataFileMeasureReader(xxx).read_all():
    #     print(_)
