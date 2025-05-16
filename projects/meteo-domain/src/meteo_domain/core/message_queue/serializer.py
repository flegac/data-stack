from abc import ABC, abstractmethod


class Serializer[Input, Output](ABC):
    @abstractmethod
    def serialize(self, message: Input) -> Output: ...

    @abstractmethod
    def deserialize(self, raw: Output) -> Input: ...
