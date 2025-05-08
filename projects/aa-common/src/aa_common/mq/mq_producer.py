from abc import abstractmethod
from collections.abc import Iterable


class MQProducer[Input]:
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

    @abstractmethod
    async def stop(self): ...
