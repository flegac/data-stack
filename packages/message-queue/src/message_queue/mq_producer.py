from abc import abstractmethod
from typing import Generic, Iterable

from message_queue.mq_topic import MQTopic
from message_queue.serializer import I, O


class MQProducer(Generic[I]):
    def __init__(self, topic: MQTopic[I, O]):
        self.topic = topic

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
