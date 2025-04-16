import asyncio

from s3_connector.s3_client import S3Client
from s3_connector.s3_config import S3Config


async def main():
    config = S3Config(
        endpoint="http://localhost:9000",
        access_key="admin",
        secret_key="adminpassword"
    )
    client = S3Client(config)

    await client.create_bucket("my-bucket")
    file_content = "Hello, MinIO!"
    await client.upload_file("my-bucket", "example.txt", file_content)
    await client.list_buckets()
    await client.list_objects("my-bucket")
    await client.get_object_metadata("my-bucket", "example.txt")
    content = await client.download_object("my-bucket", "example.txt")
    if content:
        print("Downloaded content:")
        print(content.decode("utf-8"))


if __name__ == '__main__':
    asyncio.run(main())
