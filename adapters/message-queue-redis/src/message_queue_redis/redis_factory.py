# redis_factory.py
from typing import override

from meteo_domain.core.message_queue.mq_backend import MQBackend
from meteo_domain.core.message_queue.mq_topic import MQTopic

from message_queue_redis.redis_connection import RedisConnection
from message_queue_redis.redis_consumer import RedisConsumer
from message_queue_redis.redis_producer import RedisProducer


class RedisMQBackend(MQBackend):
    def __init__(self, connection: RedisConnection):
        self.connection = connection

    @override
    def producer[I, O](self, topic: MQTopic[I, O]):
        return RedisProducer(topic, self.connection)

    @override
    def consumer[I, O](self, topic: MQTopic[I, O]):
        return RedisConsumer(topic, self.connection)
