from typing import Iterable, override

from confluent_kafka import Producer

from broker_api.broker_producer import BrokerProducer
from broker_api.serializer import Message, Data
from broker_kafka.kafka_config import KafkaConfig


class KafkaProducer(BrokerProducer[Message, Data]):
    def __init__(self, config: KafkaConfig[Message, Data]):
        self.config = config
        self.producer = Producer({
            'bootstrap.servers': config.broker_url,
            'security.protocol': 'PLAINTEXT',
            'acks': 0,
            'retries': 2,
            'queue.buffering.max.kbytes': 1024 * 1024,
            'batch.num.messages': 1024,
            'linger.ms': 25,
        })

    @override
    def write_batch(self, items: Iterable[Message]):
        try:
            for _ in items:
                self.write_single(_)
        finally:
            self.producer.flush()

    @override
    def write_single(self, item: Message):
        try:
            message = self.config.serializer.serialize(item)
            self.producer.produce(
                self.config.topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
        except Exception as e:
            print(f'Exception occurred: {e}')

    def _delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
