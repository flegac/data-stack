from typing import override

from kafka_connector.kafka_connection import KafkaConnection
from message_queue.mq_backend import MQBackend
from message_queue.mq_topic import MQTopic

from kafka_message_queue.kafka_consumer import KafkaConsumer
from kafka_message_queue.kafka_producer import KafkaProducer


class KafkaMQBackend(MQBackend):
    def __init__(self, connection: KafkaConnection):
        self.connection = connection

    @override
    def producer[I, O](self, topic: MQTopic[I, O]):
        return KafkaProducer(topic, self.connection)

    @override
    def consumer[I, O](self, topic: MQTopic[I, O]):
        return KafkaConsumer(topic, self.connection)
