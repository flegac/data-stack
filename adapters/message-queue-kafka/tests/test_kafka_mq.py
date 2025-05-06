import asyncio
from unittest import TestCase

from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.kafka_connection import KafkaConnection
from message_queue.mq_backend_checker import mq_backend_checker
from message_queue_kafka.kafka_factory import KafkaMQBackend


class TestKafkaMQBackend(TestCase):
    def test_it(self):
        backend = KafkaMQBackend(
            KafkaConnection(
                KafkaConfig(
                    broker_url="localhost:9092",
                )
            )
        )
        asyncio.run(
            mq_backend_checker(
                backend,
                message_number=3,
                timeout_sec=1.0,
            )
        )
