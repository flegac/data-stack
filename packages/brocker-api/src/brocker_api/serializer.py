from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Serializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, obj: T) -> str:
        ...

    @abstractmethod
    def deserialize(self, data: str) -> T:
        ...
