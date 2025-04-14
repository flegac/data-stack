from typing import Generic

from broker_api.serializer import Serializer, Message, Data


class KafkaConfig(Generic[Message, Data]):
    def __init__(self, broker_url: str, topic: str, group_id: str, serializer: Serializer[Message, Data]):
        self.broker_url = broker_url
        self.topic = topic
        self.group_id = group_id
        self.serializer = serializer
