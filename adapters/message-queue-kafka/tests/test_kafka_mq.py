import asyncio
import threading
import time
from unittest import IsolatedAsyncioTestCase

from message_queue.mq_topic import MQTopic
from message_queue_kafka.kafka_factory import KafkaMQFactory
from meteo_app.config import KAFKA_CONFIG


class TestKafkaMQ(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        topic = MQTopic(topic="test-topic")
        self.factory = KafkaMQFactory(KAFKA_CONFIG)
        self.producer = self.factory.producer(topic)
        self.consumer = self.factory.consumer(topic)
        self.expected_messages = [f"message-{i}" for i in range(4)]
        self.received_messages = []

    async def message_handler(self, item):
        print(f"received: {item}")
        self.received_messages.append(item)
        if len(self.received_messages) >= len(self.expected_messages):
            await self.consumer.stop()

    def producer_thread(self, producer):
        time.sleep(1.5)
        for msg in self.expected_messages:
            print(f"sending: {msg}")
            asyncio.run(producer.write_single(msg))
            time.sleep(1.0)

    async def test_listener(self):
        producer_thread = threading.Thread(
            target=self.producer_thread, args=(self.producer,)
        )
        producer_thread.start()
        await self.consumer.listen(self.message_handler)
        producer_thread.join()

        self.assertSetEqual(set(self.received_messages), set(self.expected_messages))
