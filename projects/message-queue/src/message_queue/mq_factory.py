from abc import ABC, abstractmethod

from message_queue.mq_consumer import MQConsumer
from message_queue.mq_producer import MQProducer
from message_queue.mq_topic import MQTopic


class MQFactory(ABC):
    @abstractmethod
    def producer[I, O](self, topic: MQTopic[I, O]) -> MQProducer[I]: ...

    @abstractmethod
    def consumer[I, O](self, topic: MQTopic[I, O]) -> MQConsumer[I]: ...
