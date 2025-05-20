import datetime
from abc import ABC, abstractmethod
from collections.abc import Iterable

from meteo_domain.geo_sensor.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.geo_sensor.entities.telemetry.geo_sensor_series import GeoSensorSeries
from meteo_domain.geo_sensor.entities.telemetry.region_series import RegionSeries
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry


class TSeriesRepository(ABC):
    @abstractmethod
    async def save_batch(
        self, measures: Iterable[TaggedTelemetry], chunk_size: int = 100_000
    ): ...

    @abstractmethod
    def find_at(self, time: datetime.datetime) -> GeoSensorSeries: ...

    @abstractmethod
    def search(self, query: MeasureQuery | None = None) -> RegionSeries: ...

    @abstractmethod
    async def init(self, reset: bool = False): ...
