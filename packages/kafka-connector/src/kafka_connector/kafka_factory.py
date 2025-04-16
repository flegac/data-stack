from kafka_connector.broker_topic import BrokerTopic
from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.kafka_consumer import KafkaConsumer
from kafka_connector.kafka_producer import KafkaProducer


class KafkaFactory:
    def __init__(self, config: KafkaConfig):
        self.config = config

    def producer[I, O](self, topic: BrokerTopic[I, O]):
        return KafkaProducer(topic, self.config)

    def consumer[I, O](self, topic: BrokerTopic[I, O]):
        return KafkaConsumer(topic, self.config)
