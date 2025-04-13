from abc import abstractmethod
from typing import Generic, Callable, TypeVar

T = TypeVar('T')


class BrockerConsumer(Generic[T]):

    @abstractmethod
    def listen(self, on_message: Callable[[T], None]):
        ...
