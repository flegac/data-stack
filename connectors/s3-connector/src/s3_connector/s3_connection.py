from functools import cached_property

import aioboto3
from botocore.config import Config

from s3_connector.s3_config import S3Config


class S3Connection:
    def __init__(self, config: S3Config):
        self.config = config
        self.s3_config = Config(s3={"addressing_style": "path"})

    @cached_property
    def session(self):
        return aioboto3.Session(
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region,
        )

    def client(self):
        return self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        )
