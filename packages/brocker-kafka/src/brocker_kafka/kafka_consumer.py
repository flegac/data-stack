from typing import Callable, TypeVar, override

from confluent_kafka import Consumer, KafkaError

from brocker_api.brocker_consumer import BrockerConsumer
from brocker_kafka.kafka_config import KafkaConfig

T = TypeVar('T')


class KafkaConsumer(BrockerConsumer[T]):
    def __init__(self, config: KafkaConfig[T]):
        self.config = config
        self.consumer = Consumer({
            'bootstrap.servers': config.broker_url,
            'group.id': config.group_id,
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT'
        })

    @override
    def listen(self, on_message: Callable[[T], None]):
        self.consumer.subscribe([self.config.topic])
        try:
            while True:
                msg = self.consumer.poll(.2)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                item = self.config.serializer.deserialize(msg.value().decode('utf-8'))
                on_message(item)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
