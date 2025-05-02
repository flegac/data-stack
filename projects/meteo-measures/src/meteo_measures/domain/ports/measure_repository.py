from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable

from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.measure import Measure
from meteo_measures.domain.entities.measures.measure_series import MeasureSeries


class MeasureRepository(ABC):
    @abstractmethod
    async def save_batch(self, measures: Iterable[Measure]): ...

    @abstractmethod
    async def save(self, measure: Measure): ...

    @abstractmethod
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]: ...
