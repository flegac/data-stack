from typing import Generic

from kafka_connector.serializer import I, O, Serializer


class BrokerTopic(Generic[I, O]):
    def __init__(self, topic: str, serializer: Serializer[I, O]):
        self.topic = topic
        self.serializer = serializer
