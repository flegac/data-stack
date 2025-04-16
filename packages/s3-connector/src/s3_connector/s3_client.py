from functools import cached_property
from typing import Optional

import aioboto3
from botocore.config import Config

from s3_connector.s3_config import S3Config


class S3Client:
    def __init__(self, config: S3Config):
        self.config = config
        self.s3_config = Config(s3={"addressing_style": "path"})

    @cached_property
    def session(self):
        return aioboto3.Session(
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region
        )

    async def create_bucket(self, bucket: str):
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            try:
                await s3_client.create_bucket(Bucket=bucket)
                print(f"Bucket {bucket} created successfully.")
            except s3_client.exceptions.BucketAlreadyOwnedByYou:
                print(f"Bucket {bucket} already exists.")

    async def upload_file(self, bucket: str, object_key: str, file_content: str):
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            await s3_client.put_object(Bucket=bucket, Key=object_key, Body=file_content)
            print(f"File {object_key} uploaded successfully to bucket {bucket}.")

    async def list_buckets(self):
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            response = await s3_client.list_buckets()
            print("Buckets:")
            for bucket in response["Buckets"]:
                print(f"  {bucket['Name']}")

    async def list_objects(self, bucket: str):
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            response = await s3_client.list_objects_v2(Bucket=bucket)
            print(f"Objects in bucket {bucket}:")
            if "Contents" in response:
                for obj in response["Contents"]:
                    print(f"  {obj['Key']}")
            else:
                print("  No objects found.")

    async def get_object_metadata(self, bucket: str, object_key: str):
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            response = await s3_client.head_object(Bucket=bucket, Key=object_key)
            print(f"Metadata for {object_key} in bucket {bucket}:")
            print(response)

    async def download_object(self, bucket: str, object_key: str) -> Optional[bytes]:
        async with self.session.client("s3", endpoint_url=self.config.endpoint, config=self.s3_config) as s3_client:
            response = await s3_client.get_object(Bucket=bucket, Key=object_key)
            async with response["Body"] as stream:
                return await stream.read()
