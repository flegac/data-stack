from abc import abstractmethod
from typing import Generic, Iterable

from message_queue.serializer import I


class MQProducer(Generic[I]):
    @abstractmethod
    async def write_single(self, item: I):
        ...

    async def write_batch(self, items: Iterable[I]):
        try:
            for _ in items:
                await self.write_single(_)
        finally:
            await self.flush()

    @abstractmethod
    async def flush(self):
        ...
