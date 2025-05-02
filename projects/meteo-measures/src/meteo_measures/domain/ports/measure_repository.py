from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable

from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.measure_series import MeasureSeries
from meteo_measures.domain.entities.measures.measurement import Measurement


class MeasureRepository(ABC):
    @abstractmethod
    async def save_batch(self, measures: Iterable[Measurement]): ...

    @abstractmethod
    async def save(self, measure: Measurement): ...

    @abstractmethod
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]: ...
