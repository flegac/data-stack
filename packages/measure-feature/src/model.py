from abc import ABC, abstractmethod
from typing import Generator

from measure_feature.model.sensor import MeasureType


class MeasureMetadata:
    dtype: MeasureType

class MeasureDataset:
    metadata: MeasureMetadata



class DatasetReader(ABC):
    @abstractmethod
    def read_all(self) -> Generator[MeasureDataset, None,None]:
        ...

class DatasetWriter(ABC):
    @abstractmethod
    def write_all(self, dataset : MeasureDataset):
        ...

