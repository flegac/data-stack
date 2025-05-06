from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int = 0
