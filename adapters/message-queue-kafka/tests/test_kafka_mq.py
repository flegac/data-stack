import asyncio
from unittest import IsolatedAsyncioTestCase

from aa_common.logger import logger
from kafka_connector.kafka_connection import KafkaConnection
from message_queue.mq_topic import MQTopic
from message_queue_kafka.kafka_factory import KafkaMQFactory
from meteo_app.config import KAFKA_CONFIG


class TestKafkaMQ(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.topic = MQTopic(topic="test-topic")
        connection = KafkaConnection(KAFKA_CONFIG)
        self.factory = KafkaMQFactory(connection)
        self.producer = self.factory.producer(self.topic)
        self.consumer = self.factory.consumer(self.topic)
        self.expected_messages = [f"message-{i}" for i in range(10)]
        self.received_messages = []

    async def message_handler(self, item):
        logger.debug(f"received: {item}")
        self.received_messages.append(item)

    async def produce_messages(self):
        for msg in self.expected_messages:
            logger.debug(f"sending: {msg}")
            await self.producer.write_single(msg)

    async def test_listener(self):
        consumer_task = asyncio.create_task(self.consumer.listen(self.message_handler))
        producer_task = asyncio.create_task(self.produce_messages())

        # Laisser tourner pendant 5 secondes avant d'arrêter le consumer
        await asyncio.sleep(5.0)
        await self.consumer.stop()

        # Attendre que les tâches se terminent
        await consumer_task
        await producer_task
        await self.producer.close()

        self.assertEqual(len(self.received_messages), len(self.expected_messages))
        self.assertSetEqual(set(self.received_messages), set(self.expected_messages))

    async def asyncTearDown(self):
        await self.consumer.stop()
        await self.producer.close()
