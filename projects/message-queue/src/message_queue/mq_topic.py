from typing import Generic

from message_queue.serializer import Input, Output, Serializer


# pylint: disable=too-few-public-methods
class MQTopic(Generic[Input, Output]):
    def __init__(self, topic: str, serializer: Serializer[Input, Output] = None):
        self.topic = topic
        self.serializer = serializer
