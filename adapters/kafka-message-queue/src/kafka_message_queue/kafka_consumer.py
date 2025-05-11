import traceback
from collections.abc import Awaitable, Callable
from typing import Any, override

from loguru import logger

from aa_common.mq.mq_consumer import MQConsumer
from aa_common.mq.mq_topic import MQTopic
from kafka_connector.kafka_connection import KafkaConnection


class KafkaConsumer[Input](MQConsumer[Input]):
    def __init__(self, topic: MQTopic[Input, Any], connection: KafkaConnection):
        self.topic = topic
        self.consumer = connection.consumer(topic)

    @override
    async def listen(self, on_message: Callable[[Input], Awaitable[Any]]):
        logger.info(f"listen on topic: {self.topic.topic}")
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    if serializer := self.topic.serializer:
                        item = serializer.deserialize(msg.value)
                    else:
                        item = msg.value.decode("utf-8")
                    await on_message(item)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    traceback.print_exc()
                    logger.error(f"{msg}: {e}")

        finally:
            await self.consumer.stop()

    @override
    async def stop(self):
        await self.consumer.stop()
