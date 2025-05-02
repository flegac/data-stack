from typing import override

from confluent_kafka import Producer
from loguru import logger
from message_queue.mq_producer import MQProducer
from message_queue.mq_topic import MQTopic
from message_queue.serializer import Input, Output
from message_queue_kafka.kafka_config import KafkaConfig


class KafkaProducer(MQProducer[Input]):
    def __init__(self, topic: MQTopic[Input, Output], config: KafkaConfig):
        self.topic = topic
        self.config = config
        self.producer = Producer(
            {
                "bootstrap.servers": config.broker_url,
                "security.protocol": "PLAINTEXT",
                "acks": 0,
                "retries": 2,
                "queue.buffering.max.kbytes": 1024 * 1024,
                "batch.num.messages": 1024,
                "linger.ms": 25,
            }
        )

    @override
    async def write_single(self, item: Input):
        try:
            message = self.topic.serializer.serialize(item)
            self.producer.produce(
                self.topic.topic, value=message, callback=self._delivery_report
            )
        except Exception as e:
            logger.warning(f"{self.topic.topic}: {item}: Error! {e}")

    @override
    async def flush(self):
        self.producer.flush()

    def _delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
