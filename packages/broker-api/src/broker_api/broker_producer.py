from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterable

T = TypeVar('T')


class BrokerProducer(ABC, Generic[T]):
    @abstractmethod
    def write_batch(self, items: Iterable[T]):
        ...

    @abstractmethod
    def write_single(self, item: T):
        ...
