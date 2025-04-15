from typing import override

from confluent_kafka import Producer

from broker_api.broker_producer import BrokerProducer
from broker_api.broker_topic import BrokerTopic
from broker_api.serializer import I, O
from broker_kafka.kafka_config import KafkaConfig


class KafkaProducer(BrokerProducer[I]):
    def __init__(self, topic: BrokerTopic[I, O], config: KafkaConfig):
        super().__init__(topic)
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

    @override
    def flush(self):
        self.producer.flush()

    def _delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
