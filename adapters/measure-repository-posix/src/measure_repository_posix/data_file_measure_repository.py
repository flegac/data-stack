from collections.abc import Iterable
from typing import override

import xarray as xr
from datafile_api_xarray.xarray_datafile_api import XarrayDatafileAPI
from loguru import logger
from meteo_domain.core.dates import to_datetime
from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.location.location import Location
from meteo_domain.geo_sensor.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.geo_sensor.entities.telemetry.geo_sensor_series import GeoSensorSeries
from meteo_domain.geo_sensor.entities.telemetry.region_series import RegionSeries
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry
from meteo_domain.geo_sensor.entities.telemetry.telemetry import (
    Telemetry,
)
from meteo_domain.geo_sensor.ports.tseries_repository import TSeriesRepository


class DataFileMeasureRepository(TSeriesRepository):
    def __init__(self, data_file: DataFile):
        self.api = XarrayDatafileAPI()
        self.data_file = data_file
        self.metadata = self.api.load_from_datafile(self.data_file)
        self.raw = self.api.load_raw_data(data_file)
        logger.info(f"{self.raw}")

    @override
    async def save_batch(
        self, measures: Iterable[TaggedTelemetry], chunk_size: int = 100_000
    ):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery = None) -> RegionSeries:
        # TODO: filter according to query # pylint: disable=fixme
        dataset = self.raw
        latitudes = dataset["latitude"]
        longitudes = dataset["longitude"]

        variables = [
            _
            for _ in self.metadata.variables
            if _.name not in ["latitude", "longitude"]
        ]

        series_list = []

        for variable in variables:
            try:
                for lat_idx in range(len(latitudes)):
                    for lon_idx in range(len(longitudes)):
                        series_list.append(
                            GeoSensorSeries(
                                sensor=GeoSensor(
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
                        )
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning(f"Could not handle variable=[{variable}] : {e}")
        return RegionSeries(series=series_list)

    @override
    async def init(self, reset: bool = False):
        pass

    @staticmethod
    def _extract_time_series(
        dataset: xr.Dataset, variable_name: str, lat_idx: int, lon_idx: int
    ) -> list[Telemetry]:
        data_array = dataset[variable_name].isel(latitude=lat_idx, longitude=lon_idx)
        datetime_values = data_array["times"].values.flatten()
        data_values = data_array.values.flatten()

        times = list(map(to_datetime, datetime_values))
        return [
            Telemetry(time=time, value=float(value))
            for time, value in zip(times, data_values, strict=False)
        ]
