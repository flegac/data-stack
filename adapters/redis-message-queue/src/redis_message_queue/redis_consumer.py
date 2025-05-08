from collections.abc import Awaitable, Callable
from typing import Any, override

from aa_common.logger import logger
from aa_common.mq.mq_consumer import MQConsumer
from aa_common.mq.mq_topic import MQTopic
from redis_message_queue.redis_connection import RedisConnection


class RedisConsumer[Input](MQConsumer[Input]):
    def __init__(self, topic: MQTopic[Input, Any], connection: RedisConnection):
        self.topic = topic
        self.connection = connection
        self._redis = None
        self._pubsub = None
        self._running = False

    @override
    async def listen(self, on_message: Callable[[Input], Awaitable[Any]]):
        logger.info(f"listen on topic: {self.topic.topic}")
        self._redis = await self.connection.ensure_connection()
        self._pubsub = self._redis.pubsub()

        await self._pubsub.subscribe(self.topic.topic)
        self._running = True

        try:
            while self._running:
                message = await self._pubsub.get_message(ignore_subscribe_messages=True)
                if message and message["type"] == "message":
                    try:
                        if serializer := self.topic.serializer:
                            item = serializer.deserialize(message["data"])
                        else:
                            item = message["data"]
                        await on_message(item)
                    except Exception as e:
                        logger.error(f"{message}: {e}")
        finally:
            await self.stop()

    @override
    async def stop(self):
        self._running = False
        if self._pubsub:
            await self._pubsub.unsubscribe(self.topic.topic)
            await self._pubsub.aclose()
