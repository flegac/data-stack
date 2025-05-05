from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable
from typing import Any

from meteo_domain.entities.measures.measure_query import MeasureQuery
from meteo_domain.entities.measures.measure_series import MeasureSeries
from meteo_domain.entities.measures.measurement import Measurement


class MeasureRepository(ABC):
    @abstractmethod
    async def save_batch(self, measures: Iterable[Measurement]): ...

    @abstractmethod
    async def save(self, measure: Measurement): ...

    @abstractmethod
    def search(
        self, query: MeasureQuery | None = None
    ) -> Generator[MeasureSeries, Any, None]: ...
