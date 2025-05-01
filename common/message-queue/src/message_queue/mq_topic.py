from typing import Generic

from message_queue.serializer import I, O, Serializer


class MQTopic(Generic[I, O]):
    def __init__(self, topic: str, serializer: Serializer[I, O]):
        self.topic = topic
        self.serializer = serializer
