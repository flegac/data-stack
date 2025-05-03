from abc import abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, Generic

from message_queue.serializer import Input


class MQConsumer(Generic[Input]):
    @abstractmethod
    async def listen(self, on_message: Callable[[Input], Awaitable[Any]]): ...

    @abstractmethod
    async def stop(self): ...
