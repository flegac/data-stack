from meteo_domain.core.message_queue.serializer import Serializer


# pylint: disable=too-few-public-methods
class MQTopic[Input, Output]:
    def __init__(self, topic: str, serializer: Serializer[Input, Output] = None):
        self.topic = topic
        self.serializer = serializer
