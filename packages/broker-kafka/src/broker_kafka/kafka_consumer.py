from typing import Callable, override

from confluent_kafka import Consumer, KafkaError

from broker_api.broker_consumer import BrokerConsumer
from broker_api.broker_topic import BrokerTopic
from broker_api.serializer import I, O
from broker_kafka.kafka_config import KafkaConfig


class KafkaConsumer(BrokerConsumer[I]):
    def __init__(self, topic: BrokerTopic[I, O], config: KafkaConfig):
        super().__init__(topic)
        self.config = config
        self.consumer = Consumer({
            'bootstrap.servers': config.broker_url,
            'group.id': config.group_id,
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT'
        })

    @override
    def listen(self, on_message: Callable[[I], None]):
        self.consumer.subscribe([self.topic.topic])
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
                value = msg.value()
                item = self.topic.serializer.deserialize(value.decode('utf-8'))
                on_message(item)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
