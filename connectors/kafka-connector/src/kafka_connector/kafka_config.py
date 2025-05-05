from dataclasses import dataclass


@dataclass
class KafkaConfig:
    broker_url: str
