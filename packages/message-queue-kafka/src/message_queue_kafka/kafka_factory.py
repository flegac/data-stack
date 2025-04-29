from message_queue.mq_topic import MQTopic
from message_queue_kafka.kafka_config import KafkaConfig
from message_queue_kafka.kafka_consumer import KafkaConsumer
from message_queue_kafka.kafka_producer import KafkaProducer


class KafkaFactory:
    def __init__(self, config: KafkaConfig):
        self.config = config

    def producer[I, O](self, topic: MQTopic[I, O]):
        return KafkaProducer(topic, self.config)

    def consumer[I, O](self, topic: MQTopic[I, O]):
        return KafkaConsumer(topic, self.config)
