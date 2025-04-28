import asyncio

from file_repository_s3.s3_file_repository import S3FileRepository
from file_repository_s3.s3_config import S3Config


async def main():
    config = S3Config(
        endpoint="http://localhost:9000",
        access_key="admin",
        secret_key="adminpassword"
    )
    repository = S3FileRepository(config)

    await repository.create_bucket("my-bucket")
    file_content = "Hello, MinIO!"
    await repository.upload_file("my-bucket", "example.txt", file_content)
    await repository.list_buckets()
    await repository.list_files("my-bucket")
    await repository.get_object_metadata("my-bucket", "example.txt")
    content = await repository.download_file("my-bucket", "example.txt")
    if content:
        print("Downloaded content:")
        print(content.decode("utf-8"))


if __name__ == '__main__':
    asyncio.run(main())
