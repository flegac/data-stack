from abc import abstractmethod
from typing import Generic, Callable

from broker_api.broker_topic import BrokerTopic
from broker_api.serializer import I, O


class BrokerConsumer(Generic[I]):
    def __init__(self, topic: BrokerTopic[I, O]):
        self.topic = topic

    @abstractmethod
    def listen(self, on_message: Callable[[I], None]):
        ...
