import asyncio
import threading
import time
from unittest import IsolatedAsyncioTestCase

from message_queue.memory_mq_factory import MemoryMQFactory
from message_queue.mq_topic import MQTopic


class TestMemoryMQ(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        topic = MQTopic(topic="test-topic")
        self.factory = MemoryMQFactory()
        self.producer = self.factory.producer(topic)
        self.consumer = self.factory.consumer(topic)
        self.expected_messages = [f"message-{i}" for i in range(10)]
        self.received_messages = []

    async def message_handler(self, item):
        self.received_messages.append(item)
        if len(self.received_messages) >= len(self.expected_messages):
            await self.consumer.stop()

    def producer_thread(self, producer):
        for msg in self.expected_messages:
            asyncio.run(producer.write_single(msg))
            time.sleep(0.5)

    async def test_listener(self):
        producer_thread = threading.Thread(
            target=self.producer_thread, args=(self.producer,)
        )
        producer_thread.start()
        await self.consumer.listen(self.message_handler)
        producer_thread.join()

        self.assertEqual(self.received_messages, self.expected_messages)
