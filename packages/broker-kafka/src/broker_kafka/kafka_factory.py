from broker_api.broker_topic import BrokerTopic
from broker_kafka.kafka_config import KafkaConfig
from broker_kafka.kafka_consumer import KafkaConsumer
from broker_kafka.kafka_producer import KafkaProducer


class KafkaFactory:
    def __init__(self, config: KafkaConfig):
        self.config = config

    def producer[I, O](self, topic: BrokerTopic[I, O]):
        return KafkaProducer(topic, self.config)

    def consumer[I, O](self, topic: BrokerTopic[I, O]):
        return KafkaConsumer(topic, self.config)
