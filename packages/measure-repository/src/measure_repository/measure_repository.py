from abc import ABC, abstractmethod
from typing import Generator, Any

from measure_repository.measure_query import MeasureQuery
from measure_repository.model.measure import Measure
from measure_repository.model.measure_series import MeasureSeries


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
