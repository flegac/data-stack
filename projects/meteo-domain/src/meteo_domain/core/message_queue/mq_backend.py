from abc import ABC, abstractmethod

from meteo_domain.core.message_queue.mq_consumer import MQConsumer
from meteo_domain.core.message_queue.mq_producer import MQProducer
from meteo_domain.core.message_queue.mq_topic import MQTopic


class MQBackend(ABC):
    @abstractmethod
    def producer[I, O](self, topic: MQTopic[I, O]) -> MQProducer[I]: ...

    @abstractmethod
    def consumer[I, O](self, topic: MQTopic[I, O]) -> MQConsumer[I]: ...
