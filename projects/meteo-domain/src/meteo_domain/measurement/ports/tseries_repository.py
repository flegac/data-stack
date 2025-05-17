from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable
from typing import Any

from meteo_domain.measurement.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.measurement.entities.measurement import (
    TaggedMeasurement,
)
from meteo_domain.measurement.entities.temporal_series import TSeries


class TSeriesRepository(ABC):
    @abstractmethod
    async def save_batch(
        self, measures: Iterable[TaggedMeasurement], chunk_size: int = 100_000
    ): ...

    @abstractmethod
    def search(self, query: MeasureQuery | None = None) -> Generator[TSeries, Any]: ...

    @abstractmethod
    async def init(self, reset: bool = False): ...
