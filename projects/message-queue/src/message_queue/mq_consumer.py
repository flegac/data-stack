from abc import abstractmethod
from typing import Any, Awaitable, Callable, Generic

from message_queue.serializer import Input


class MQConsumer(Generic[Input]):
    @abstractmethod
    async def listen(self, on_message: Callable[[Input], Awaitable[Any]]): ...
