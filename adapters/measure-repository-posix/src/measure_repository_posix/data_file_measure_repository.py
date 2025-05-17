import datetime
from collections.abc import Generator, Iterable
from typing import Any, override

import numpy as np
import xarray as xr
from loguru import logger

from datafile_api_xarray.xarray_datafile_api import XarrayDatafileAPI
from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.measurement.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.measurement.entities.measurement import (
    Measurement,
    TaggedMeasurement,
)
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor
from meteo_domain.measurement.entities.temporal_series import TSeries
from meteo_domain.measurement.ports.tseries_repository import TSeriesRepository


class DataFileMeasureRepository(TSeriesRepository):
    def __init__(self, data_file: DataFile):
        self.api = XarrayDatafileAPI()
        self.data_file = data_file
        self.metadata = self.api.load_from_datafile(self.data_file)
        self.raw = self.api.load_raw_data(data_file)
        logger.info(f"{self.raw}")

    @override
    async def save_batch(
        self, measures: Iterable[TaggedMeasurement], chunk_size: int = 100_000
    ):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery = None) -> Generator[TSeries, Any]:
        # TODO: filter according to query # pylint: disable=fixme
        dataset = self.raw
        latitudes = dataset["latitude"]
        longitudes = dataset["longitude"]

        variables = [
            _
            for _ in self.metadata.variables
            if _.name not in ["latitude", "longitude"]
        ]

        for variable in variables:
            try:
                for lat_idx in range(len(latitudes)):
                    for lon_idx in range(len(longitudes)):
                        temperatures = TSeries(
                            sensor=Sensor(
                                uid="cds",
                                measure_type=variable.name,
                                location=Location(
                                    latitude=float(latitudes.values[lat_idx]),
                                    longitude=float(longitudes.values[lon_idx]),
                                ),
                            ),
                            measures=self._extract_time_series(
                                dataset, variable.name, lat_idx, lon_idx
                            ),
                        )
                        yield temperatures
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning(f"Could not handle variable=[{variable}] : {e}")

    @override
    async def init(self, reset: bool = False):
        pass

    @staticmethod
    def _extract_time_series(
        dataset: xr.Dataset, variable_name: str, lat_idx: int, lon_idx: int
    ) -> list[Measurement]:
        data_array = dataset[variable_name].isel(latitude=lat_idx, longitude=lon_idx)
        datetime_values = data_array["time"].values.flatten()
        data_values = data_array.values.flatten()

        times = list(map(to_datetime, datetime_values))
        return [
            Measurement(time=time, value=float(value))
            for time, value in zip(times, data_values, strict=False)
        ]


def to_datetime(date: np.datetime64) -> datetime.datetime:
    """
    https://gist.github.com/blaylockbk/1677b446bc741ee2db3e943ab7e4cabd?permalink_comment_id=3775327

    Converts a numpy datetime64 object to a python datetime object
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = (date - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    return datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
