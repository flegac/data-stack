from typing import Callable, Awaitable, Any, override

from aiokafka import AIOKafkaConsumer

from message_queue.mq_consumer import MQConsumer
from message_queue.mq_topic import MQTopic
from message_queue.serializer import I, O
from message_queue_kafka.kafka_config import KafkaConfig


class KafkaConsumer(MQConsumer[I]):
    def __init__(self, topic: MQTopic[I, O], config: KafkaConfig):
        super().__init__(topic)
        self.config = config
        self.consumer = AIOKafkaConsumer(
            self.topic.topic,
            bootstrap_servers=config.broker_url,
            group_id=config.group_id,
            auto_offset_reset='earliest',
            # value_deserializer=lambda x: x.decode('utf-8')
        )

    @override
    async def listen(self, on_message: Callable[[I], Awaitable[Any]]):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                item = self.topic.serializer.deserialize(msg.value)
                await on_message(item)
        finally:
            await self.consumer.stop()
