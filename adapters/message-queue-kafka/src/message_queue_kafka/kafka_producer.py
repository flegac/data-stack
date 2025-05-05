from typing import override

from loguru import logger

from kafka_connector.kafka_connection import KafkaConnection
from message_queue.mq_producer import MQProducer
from message_queue.mq_topic import MQTopic
from message_queue.serializer import Input, Output


class KafkaProducer(MQProducer[Input]):
    def __init__(self, topic: MQTopic[Input, Output], connection: KafkaConnection):
        self.topic = topic
        self.producer = connection.producer()

    @override
    async def write_single(self, item: Input):
        try:
            if serializer := self.topic.serializer:
                message = serializer.serialize(item)
            else:
                message = item
            self.producer.produce(
                self.topic.topic, value=message, callback=_delivery_report
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(f"{self.topic.topic}: {item}: Error! {e}")

    @override
    async def flush(self):
        self.producer.flush()


def _delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
