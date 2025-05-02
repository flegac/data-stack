from typing import override

from message_queue.mq_factory import MQFactory
from message_queue.mq_topic import MQTopic
from message_queue_kafka.kafka_config import KafkaConfig
from message_queue_kafka.kafka_consumer import KafkaConsumer
from message_queue_kafka.kafka_producer import KafkaProducer


class KafkaMQFactory(MQFactory):
    def __init__(self, config: KafkaConfig):
        self.config = config

    @override
    def producer[I, O](self, topic: MQTopic[I, O]):
        return KafkaProducer(topic, self.config)

    @override
    def consumer[I, O](self, topic: MQTopic[I, O]):
        return KafkaConsumer(topic, self.config)
