from abc import abstractmethod
from typing import Callable, Awaitable, Any, Generic

from message_queue.mq_topic import MQTopic
from message_queue.serializer import I, O


class MQConsumer(Generic[I]):
    def __init__(self, topic: MQTopic[I, O]):
        self.topic = topic

    @abstractmethod
    async def listen(self, on_message: Callable[[I], Awaitable[Any]]):
        ...
