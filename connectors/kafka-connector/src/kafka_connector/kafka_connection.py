from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from kafka_connector.kafka_config import KafkaConfig
from message_queue.mq_topic import MQTopic
from message_queue.serializer import Input, Output


class KafkaConnection:
    def __init__(self, config: KafkaConfig):
        self.config = config

    def consumer(
        self,
        topic: MQTopic[Input, Output],
        group_id: str = None,
        auto_offset_reset="latest",
    ):
        return AIOKafkaConsumer(
            topic.topic,
            bootstrap_servers=self.config.broker_url,
            auto_offset_reset=auto_offset_reset,
            group_id=group_id,
        )

    def producer(self):
        return AIOKafkaProducer(
            bootstrap_servers=self.config.broker_url,
            acks=0,
            request_timeout_ms=2000,
            retry_backoff_ms=100,
            max_batch_size=1024 * 1024,
            linger_ms=25,
        )
