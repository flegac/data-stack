import asyncio

from meteo_domain.core.logger import logger
from meteo_domain.core.message_queue.mq_backend import MQBackend
from meteo_domain.core.message_queue.mq_topic import MQTopic


async def mq_backend_checker(
    mq_factory: MQBackend,
    message_number: int = 3,
    timeout_sec: float = 0.5,
):
    topic = MQTopic(topic="test-topic")
    producer = mq_factory.producer(topic)
    consumer = mq_factory.consumer(topic)
    expected_messages = [f"message-{i}" for i in range(message_number)]
    received_messages = []

    async def message_handler(item):
        logger.debug(f"received: {item}")
        received_messages.append(item)

    async def produce_messages():
        for msg in expected_messages:
            logger.debug(f"sending: {msg}")
            await producer.write_single(msg)

    consumer_task = asyncio.create_task(consumer.listen(message_handler))
    await asyncio.sleep(0.5)

    producer_task = asyncio.create_task(produce_messages())

    await asyncio.sleep(timeout_sec)
    await consumer.stop()
    await consumer_task
    await producer_task
    await producer.stop()

    assert len(received_messages) == len(expected_messages)
    assert set(received_messages) == set(expected_messages)
