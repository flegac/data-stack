from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable
from typing import Any

from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measure_series import MeasureSeries
from meteo_domain.entities.measurement.measurement import Measurement


class MeasureRepository(ABC):
    @abstractmethod
    async def save_batch(
        self, measures: Iterable[Measurement], chunk_size: int = 100_000
    ): ...

    async def save(self, measure: Measurement):
        return await self.save_batch([measure])

    @abstractmethod
    def search(
        self, query: MeasureQuery | None = None
    ) -> Generator[MeasureSeries, Any]: ...

    @abstractmethod
    async def init(self, reset: bool = False): ...
