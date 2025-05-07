from abc import ABC, abstractmethod

from aa_common.mq.mq_consumer import MQConsumer
from aa_common.mq.mq_producer import MQProducer
from aa_common.mq.mq_topic import MQTopic


class MQBackend(ABC):
    @abstractmethod
    def producer[I, O](self, topic: MQTopic[I, O]) -> MQProducer[I]: ...

    @abstractmethod
    def consumer[I, O](self, topic: MQTopic[I, O]) -> MQConsumer[I]: ...
