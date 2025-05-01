from abc import abstractmethod
from typing import Callable, Awaitable, Any, Generic

from message_queue.serializer import I


class MQConsumer(Generic[I]):
    @abstractmethod
    async def listen(self, on_message: Callable[[I], Awaitable[Any]]):
        ...
