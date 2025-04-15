from typing import Generic

from broker_api.serializer import I, O, Serializer


class BrokerTopic(Generic[I, O]):
    def __init__(self, topic: str, serializer: Serializer[I, O]):
        self.topic = topic
        self.serializer = serializer
