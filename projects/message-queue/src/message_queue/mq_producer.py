from abc import abstractmethod
from typing import Generic, Iterable

from message_queue.serializer import Input


class MQProducer(Generic[Input]):
    @abstractmethod
    async def write_single(self, item: Input): ...

    async def write_batch(self, items: Iterable[Input]):
        try:
            for _ in items:
                await self.write_single(_)
        finally:
            await self.flush()

    @abstractmethod
    async def flush(self): ...
