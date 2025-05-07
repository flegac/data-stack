# redis_factory.py
from typing import override

from aa_common.mq.mq_backend import MQBackend
from aa_common.mq.mq_topic import MQTopic
from redis_message_queue.redis_connection import RedisConnection
from redis_message_queue.redis_consumer import RedisConsumer
from redis_message_queue.redis_producer import RedisProducer


class RedisMQBackend(MQBackend):
    def __init__(self, connection: RedisConnection):
        self.connection = connection

    @override
    def producer[I, O](self, topic: MQTopic[I, O]):
        return RedisProducer(topic, self.connection)

    @override
    def consumer[I, O](self, topic: MQTopic[I, O]):
        return RedisConsumer(topic, self.connection)
