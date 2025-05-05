import traceback
from typing import override

from loguru import logger

from kafka_connector.kafka_connection import KafkaConnection
from message_queue.mq_producer import MQProducer
from message_queue.mq_topic import MQTopic
from message_queue.serializer import Input, Output


class KafkaProducer(MQProducer[Input]):
    def __init__(self, topic: MQTopic[Input, Output], connection: KafkaConnection):
        self.topic = topic
        self.producer = connection.producer()
        self._started = False

    @override
    async def write_single(self, item: Input):
        await self.ensure_started()

        try:
            if serializer := self.topic.serializer:
                message = serializer.serialize(item)
            elif isinstance(item, str):
                message = item.encode("utf-8")
            else:
                message = item
            await self.producer.send_and_wait(self.topic.topic, message)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning(f"{self.topic.topic}: {item}: Error! {e}")
            logger.error(
                f"{self.topic.topic}: {item}: Error! {e}\n"
                f"{''.join(traceback.format_exception(type(e), e, e.__traceback__))}"
            )

    @override
    async def flush(self):
        if self._started:
            await self.producer.flush()

    async def ensure_started(self):
        if not self._started:
            await self.producer.start()
            self._started = True

    async def close(self):
        if self._started:
            await self.producer.stop()
            self._started = False
