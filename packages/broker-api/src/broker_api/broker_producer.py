from abc import ABC, abstractmethod
from typing import Generic, Iterable

from broker_api.broker_topic import BrokerTopic
from broker_api.serializer import I, O


class BrokerProducer(ABC, Generic[I]):
    def __init__(self, topic: BrokerTopic[I, O]):
        self.topic = topic

    @abstractmethod
    def write_single(self, item: I):
        ...

    @abstractmethod
    def flush(self):
        ...

    def write_batch(self, items: Iterable[I]):
        try:
            for _ in items:
                self.write_single(_)
        finally:
            self.flush()
