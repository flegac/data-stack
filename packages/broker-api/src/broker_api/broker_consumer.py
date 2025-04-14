from abc import abstractmethod
from typing import Generic, Callable, TypeVar

T = TypeVar('T')


class BrokerConsumer(Generic[T]):

    @abstractmethod
    def listen(self, on_message: Callable[[T], None]):
        ...
