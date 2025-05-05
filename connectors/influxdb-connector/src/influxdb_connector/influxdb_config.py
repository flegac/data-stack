from dataclasses import dataclass


@dataclass
class InfluxDBConfig:
    url: str
    org: str
    token: str
    bucket: str
