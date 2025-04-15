from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer

from broker_api.broker_consumer import BrokerConsumer
from broker_api.broker_topic import BrokerTopic
from broker_api.serializer import I, O
from broker_kafka.kafka_config import KafkaConfig


class KafkaConsumer(BrokerConsumer[I]):
    def __init__(self, topic: BrokerTopic[I, O], config: KafkaConfig):
        super().__init__(topic)
        self.config = config
        self.consumer = AIOKafkaConsumer(
            self.topic.topic,
            bootstrap_servers=config.broker_url,
            group_id=config.group_id,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: x.decode('utf-8')
        )

    async def listen(self, on_message: Callable[[I], Awaitable[None]]):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                item = self.topic.serializer.deserialize(msg.value)
                await on_message(item)
        finally:
            await self.consumer.stop()
