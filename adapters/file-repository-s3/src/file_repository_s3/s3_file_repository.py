from collections.abc import AsyncGenerator
from pathlib import Path
from typing import IO, Any, override

from loguru import logger
from meteo_domain.datafile_ingestion.ports.uow.file_repository import FileRepository
from s3_connector.s3_connection import S3Connection


class S3FileRepository(FileRepository):
    def __init__(
        self, connection: S3Connection, local_path: Path, bucket: str | None = None
    ):
        super().__init__(local_path, bucket)
        self.connection = connection

    @override
    async def create_bucket(self, bucket: str = None):
        if bucket is None:
            bucket = self.current_bucket()
        async with self.connection.client() as s3_client:
            try:
                await s3_client.head_bucket(Bucket=bucket)
                logger.info(f'Bucket "{bucket}" already exists.')
            except s3_client.exceptions.ClientError:
                logger.info(f'Bucket "{bucket}" not found: creating it ...')
                try:
                    await s3_client.create_bucket(Bucket=bucket)
                    logger.info(f'Bucket "{bucket}" created successfully.')
                except s3_client.exceptions.BucketAlreadyOwnedByYou:
                    pass
                except Exception as e:  # pylint: disable=broad-exception-caught
                    logger.info(f'Bucket "{bucket}": {e}')

    @override
    async def delete_bucket(self, bucket: str = None):
        raise NotImplementedError

    @override
    async def upload_file(self, file_id: str, file_content: bytes | IO):
        await self.create_bucket()

        bucket = self.current_bucket()
        try:
            async with self.connection.client() as s3_client:
                await s3_client.put_object(
                    Bucket=bucket, Key=file_id, Body=file_content
                )
                logger.info(
                    f'File "{file_id}" uploaded successfully to bucket {bucket}.'
                )
        except Exception as e:
            logger.error(f"Bucket {bucket}: {e}")
            raise e

    @override
    async def read_content(self, file_id: str) -> bytes | None:
        bucket = self.current_bucket()
        async with self.connection.client() as s3_client:
            response = await s3_client.get_object(Bucket=bucket, Key=file_id)
            async with response["Body"] as stream:
                return await stream.read()

    @override
    async def list_buckets(self):
        async with self.connection.client() as s3_client:
            response = await s3_client.list_buckets()
            for bucket in response["Buckets"]:
                name: str = bucket["Name"]
                yield name

    @override
    async def list_files(self) -> AsyncGenerator[str, Any]:
        bucket = self.current_bucket()
        async with self.connection.client() as s3_client:
            response = await s3_client.list_objects_v2(Bucket=bucket)
            if "Contents" in response:
                for obj in response["Contents"]:
                    name = obj["Key"]
                    yield name

    async def get_object_metadata(self, object_key: str):
        bucket = self.current_bucket()
        async with self.connection.client() as s3_client:
            response = await s3_client.head_object(Bucket=bucket, Key=object_key)
            logger.info(f"Metadata for {object_key} in bucket {bucket}:")
            logger.info(response)
