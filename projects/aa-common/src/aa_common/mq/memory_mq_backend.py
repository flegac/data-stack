import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any, override

from aa_common.mq.mq_backend import MQBackend
from aa_common.mq.mq_consumer import MQConsumer
from aa_common.mq.mq_producer import MQProducer
from aa_common.mq.mq_topic import MQTopic


class MemoryMQProducer[Input](MQProducer[Input]):
    def __init__(self, queue: list[Input]):
        self.queue = queue

    @override
    async def write_single(self, item: Input):
        self.queue.append(item)

    @override
    async def flush(self):
        pass

    @override
    async def stop(self):
        pass


class MemoryMQConsumer[Input](MQConsumer[Input]):
    def __init__(self, queue: list[Input]):
        self.queue = queue
        self._running = False

    @override
    async def listen(self, on_message: Callable[[Input], Awaitable[Any]]):
        self._running = True
        while self._running:
            if self.queue:
                message = self.queue.pop(0)  # Retire et récupère le premier message
                await on_message(message)
            else:
                await asyncio.sleep(0.1)

    @override
    async def stop(self):
        self._running = False


class MemoryMQBackend(MQBackend):
    def __init__(self):
        self.topics: dict[str, list] = defaultdict(list)

    @override
    def consumer[I, O](self, topic: MQTopic[I, O]):
        return MemoryMQConsumer(self.topics[topic.topic])

    @override
    def producer[I, O](self, topic: MQTopic[I, O]):
        return MemoryMQProducer(self.topics[topic.topic])
