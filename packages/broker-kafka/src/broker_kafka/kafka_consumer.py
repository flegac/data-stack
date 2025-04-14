from typing import Callable, override

from confluent_kafka import Consumer, KafkaError

from broker_api.broker_consumer import BrokerConsumer
from broker_api.serializer import Message, Data
from broker_kafka.kafka_config import KafkaConfig


class KafkaConsumer(BrokerConsumer[Message, Data]):
    def __init__(self, config: KafkaConfig[Message, Data]):
        self.config = config
        self.consumer = Consumer({
            'bootstrap.servers': config.broker_url,
            'group.id': config.group_id,
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT'
        })

    @override
    def listen(self, on_message: Callable[[Message], None]):
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
