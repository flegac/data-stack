from typing import Generic, TypeVar

from brocker_api.serializer import Serializer

T = TypeVar('T')


class KafkaConfig(Generic[T]):
    def __init__(self, broker_url: str, topic: str, group_id: str, serializer: Serializer[T]):
        self.broker_url = broker_url
        self.topic = topic
        self.group_id = group_id
        self.serializer = serializer
