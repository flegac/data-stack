from abc import ABC, abstractmethod
from typing import TypeVar, Generic

I = TypeVar('I')
O = TypeVar('O')


class Serializer(ABC, Generic[I, O]):
    @abstractmethod
    def serialize(self, message: I) -> O:
        ...

    @abstractmethod
    def deserialize(self, raw: O) -> I:
        ...
