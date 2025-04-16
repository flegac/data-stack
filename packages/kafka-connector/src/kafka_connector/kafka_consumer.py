from typing import Callable, Awaitable, Any, Generic

from aiokafka import AIOKafkaConsumer

from kafka_connector.broker_topic import BrokerTopic
from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.serializer import I, O


class KafkaConsumer(Generic[I]):
    def __init__(self, topic: BrokerTopic[I, O], config: KafkaConfig):
        self.topic = topic
        self.config = config
        self.consumer = AIOKafkaConsumer(
            self.topic.topic,
            bootstrap_servers=config.broker_url,
            group_id=config.group_id,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )

    async def listen(self, on_message: Callable[[I], Awaitable[Any]]):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                item = self.topic.serializer.deserialize(msg.value)
                await on_message(item)
        finally:
            await self.consumer.stop()
