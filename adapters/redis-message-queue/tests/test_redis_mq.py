import asyncio
from unittest import TestCase

from message_queue.mq_backend_checker import mq_backend_checker
from message_queue_redis.redis_config import RedisConfig
from message_queue_redis.redis_connection import RedisConnection
from message_queue_redis.redis_factory import RedisMQBackend


class TestRedisMQBackend(TestCase):
    def test_it(self):
        backend = RedisMQBackend(
            RedisConnection(
                RedisConfig(
                    host="localhost",
                    port=6379,
                    db=0,
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
