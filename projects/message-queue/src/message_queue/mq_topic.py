from typing import Generic

from message_queue.serializer import Input, Output, Serializer


class MQTopic(Generic[Input, Output]):
    def __init__(self, topic: str, serializer: Serializer[Input, Output]):
        self.topic = topic
        self.serializer = serializer
