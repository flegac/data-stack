from abc import ABC, abstractmethod
from typing import Generator, Any

from meteo_measures.entities.measures.measure import Measure
from meteo_measures.entities.measures.measure_query import MeasureQuery
from meteo_measures.entities.measures.measure_series import MeasureSeries


class MeasureRepository(ABC):

    @abstractmethod
    async def save_batch(self, measures: MeasureSeries):
        ...

    @abstractmethod
    async def save(self, measure: Measure):
        ...

    @abstractmethod
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]:
        ...
