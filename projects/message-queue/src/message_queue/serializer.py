from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Serializer(ABC, Generic[Input, Output]):
    @abstractmethod
    def serialize(self, message: Input) -> Output: ...

    @abstractmethod
    def deserialize(self, raw: Output) -> Input: ...
