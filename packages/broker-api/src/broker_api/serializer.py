from abc import ABC, abstractmethod
from typing import TypeVar, Generic

Message = TypeVar('Message')
Data = TypeVar('Data')


class Serializer(ABC, Generic[Message, Data]):
    @abstractmethod
    def serialize(self, message: Message) -> Data:
        ...

    @abstractmethod
    def deserialize(self, data: Data) -> Message:
        ...
