from dataclasses import dataclass


@dataclass
class S3Config:
    endpoint: str
    access_key: str
    secret_key: str
    region: str = "us-east-1"
