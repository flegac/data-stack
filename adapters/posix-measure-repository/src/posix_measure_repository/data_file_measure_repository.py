import time
from collections.abc import Generator, Iterable
from typing import Any, override

import pandas as pd
import xarray as xr
from loguru import logger
from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.measures.location import Location
from meteo_domain.entities.measures.measure_query import MeasureQuery
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement
from meteo_domain.entities.measures.sensor import Sensor
from meteo_domain.ports.measure_repository import MeasureRepository


class DataFileMeasureRepository(MeasureRepository):
    def __init__(self, data_file: DataFile):
        self.data_file = data_file
        self.show_config()

    def show_config(self):
        logger.info(self.data_file.raw)
        time.sleep(0.1)

    @override
    async def save_batch(self, measures: Iterable[Measurement]):
        raise NotImplementedError

    @override
    async def save(self, measure: Measurement):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery = None) -> Generator[MeasureSeries, Any, None]:
        # TODO: filter according to query # pylint: disable=fixme
        dataset = self.data_file.raw
        latitudes = dataset["latitude"]
        longitudes = dataset["longitude"]

        variables = [
            _ for _ in self.data_file.variables if _ not in ["latitude", "longitude"]
        ]

        for variable in variables:
            try:
                for lat_idx in range(len(latitudes)):
                    for lon_idx in range(len(longitudes)):
                        temperatures = MeasureSeries(
                            sensor=Sensor(
                                id="cds",
                                type=variable,
                                location=Location(
                                    latitude=float(latitudes.values[lat_idx]),
                                    longitude=float(longitudes.values[lon_idx]),
                                ),
                            ),
                            measures=self._extract_time_series(
                                dataset, variable, lat_idx, lon_idx
                            ),
                        )
                        yield temperatures
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning(f"Could not handle variable=[{variable}] : {e}")

    @staticmethod
    def _extract_time_series(
        dataset: xr.Dataset, variable_name: str, lat_idx: int, lon_idx: int
    ) -> pd.DataFrame:
        data_array = dataset[variable_name].isel(latitude=lat_idx, longitude=lon_idx)
        datetime_values = dataset["time"].values
        data_values = data_array.values.flatten()
        df = pd.DataFrame({"datetime": datetime_values, "value": data_values})
        return df
