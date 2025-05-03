from functools import cached_property
from pathlib import Path
from typing import IO, override

import aioboto3
from botocore.config import Config
from loguru import logger
from meteo_measures.domain.ports.file_repository import FileRepository

from file_repository_s3.s3_config import S3Config


class S3FileRepository(FileRepository):
    def __init__(self, config: S3Config, local_path: Path, bucket: str | None = None):
        super().__init__(local_path, bucket)
        self.config = config
        self.s3_config = Config(s3={"addressing_style": "path"})

    @cached_property
    def session(self):
        return aioboto3.Session(
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region,
        )

    @override
    async def create_bucket(self):
        bucket = self.current_bucket()
        async with self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        ) as s3_client:
            try:
                await s3_client.create_bucket(Bucket=bucket)
                print(f"Bucket {bucket} created successfully.")
            except s3_client.exceptions.BucketAlreadyOwnedByYou:
                pass
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Bucket {bucket}: {e}")

    @override
    async def upload_file(self, file_id: str, file_content: bytes | IO):
        bucket = self.current_bucket()
        try:
            async with self.session.client(
                "s3", endpoint_url=self.config.endpoint, config=self.s3_config
            ) as s3_client:
                await s3_client.put_object(
                    Bucket=bucket, Key=file_id, Body=file_content
                )
                logger.info(f"File {file_id} uploaded successfully to bucket {bucket}.")
        except Exception as e:
            logger.error(f"Bucket {bucket}: {e}")
            raise e

    @override
    async def read_content(self, file_id: str) -> bytes | None:
        bucket = self.current_bucket()
        async with self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        ) as s3_client:
            response = await s3_client.get_object(Bucket=bucket, Key=file_id)
            async with response["Body"] as stream:
                return await stream.read()

    @override
    async def list_buckets(self):
        async with self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        ) as s3_client:
            response = await s3_client.list_buckets()
            for bucket in response["Buckets"]:
                name: str = bucket["Name"]
                yield name

    @override
    async def list_files(self):
        bucket = self.current_bucket()
        async with self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        ) as s3_client:
            response = await s3_client.list_objects_v2(Bucket=bucket)
            if "Contents" in response:
                for obj in response["Contents"]:
                    name = obj["Key"]
                    yield name

    async def get_object_metadata(self, object_key: str):
        bucket = self.current_bucket()
        async with self.session.client(
            "s3", endpoint_url=self.config.endpoint, config=self.s3_config
        ) as s3_client:
            response = await s3_client.head_object(Bucket=bucket, Key=object_key)
            logger.info(f"Metadata for {object_key} in bucket {bucket}:")
            logger.info(response)
