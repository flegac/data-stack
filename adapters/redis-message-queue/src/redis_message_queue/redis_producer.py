import json
import traceback
from typing import Any, override

from aa_common.logger import logger
from aa_common.mq.mq_producer import MQProducer
from aa_common.mq.mq_topic import MQTopic

from redis_message_queue.redis_connection import RedisConnection


class RedisProducer[Input](MQProducer[Input]):
    def __init__(self, topic: MQTopic[Input, Any], connection: RedisConnection):
        self.topic = topic
        self.connection = connection
        self._started = False
        self._redis = None

    async def ensure_started(self):
        if not self._started:
            self._redis = await self.connection.ensure_connection()
            self._started = True

    @override
    async def write_single(self, item: Input):
        await self.ensure_started()

        try:
            if serializer := self.topic.serializer:
                message = serializer.serialize(item)
            elif isinstance(item, str):
                message = item
            else:
                message = json.dumps(item)

            await self._redis.publish(self.topic.topic, message)

        except Exception as e:
            logger.warning(f"{self.topic.topic}: {item}: Error! {e}")
            logger.error(
                f"{self.topic.topic}: {item}: Error! {e}\n"
                f"{''.join(traceback.format_exception(type(e), e, e.__traceback__))}"
            )

    @override
    async def flush(self):
        # Redis pubsub est immédiat, pas besoin de flush
        pass

    async def stop(self):
        if self._started and self._redis:
            await self._redis.aclose()
            self._started = False
