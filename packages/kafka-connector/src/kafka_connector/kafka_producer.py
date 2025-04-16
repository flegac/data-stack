from typing import Generic, Iterable

from confluent_kafka import Producer

from kafka_connector.broker_topic import BrokerTopic
from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.serializer import I, O


class KafkaProducer(Generic[I]):
    def __init__(self, topic: BrokerTopic[I, O], config: KafkaConfig):
        self.topic = topic
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

    def write_single(self, item: I):
        try:
            message = self.topic.serializer.serialize(item)
            self.producer.produce(
                self.topic.topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
        except Exception as e:
            print(f'Exception occurred: {e}')

    def write_batch(self, items: Iterable[I]):
        try:
            for _ in items:
                self.write_single(_)
        finally:
            self.flush()

    def flush(self):
        self.producer.flush()

    def _delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
