from aiokafka import AIOKafkaConsumer
from confluent_kafka import Producer

from kafka_connector.kafka_config import KafkaConfig
from message_queue.mq_topic import MQTopic
from message_queue.serializer import Input, Output


class KafkaConnection:
    def __init__(self, config: KafkaConfig):
        self.config = config

    def consumer(self, topic: MQTopic[Input, Output], group_id: str = None):
        return AIOKafkaConsumer(
            topic.topic,
            bootstrap_servers=self.config.broker_url,
            auto_offset_reset="earliest",
            group_id=group_id,
        )

    def producer(self):
        return Producer(
            {
                "bootstrap.servers": self.config.broker_url,
                "security.protocol": "PLAINTEXT",
                "acks": 0,
                "retries": 2,
                "queue.buffering.max.kbytes": 1024 * 1024,
                "batch.num.messages": 1024,
                "linger.ms": 25,
            }
        )
