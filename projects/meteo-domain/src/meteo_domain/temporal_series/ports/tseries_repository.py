from collections.abc import Generator, Iterable
from typing import Any, Protocol

from meteo_domain.temporal_series.entities.measure_query import MeasureQuery
from meteo_domain.temporal_series.entities.measurement import TaggedMeasurement
from meteo_domain.temporal_series.entities.temporal_series import TSeries


class TSeriesRepository(Protocol):
    async def save_batch(
        self, measures: Iterable[TaggedMeasurement], chunk_size: int = 100_000
    ): ...

    def search(self, query: MeasureQuery | None = None) -> Generator[TSeries, Any]: ...

    async def init(self, reset: bool = False): ...
