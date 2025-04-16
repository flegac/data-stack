from dataclasses import dataclass


@dataclass
class KafkaConfig:
    broker_url: str
    group_id: str
