import asyncio
from pathlib import Path

from data_file_ingestion.data_file_ingestion_service import DataFileIngestionService
from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository
from file_repository_s3.s3_file_repository import S3FileRepository
from message_queue_kafka.kafka_factory import KafkaFactory
from src.config import KAFKA_CONFIG, POSTGRE_URl, S3_CONFIG


async def main():
    service = DataFileIngestionService(
        data_file_repository=PgDataFileRepository(POSTGRE_URl),
        file_repository=S3FileRepository(
            config=S3_CONFIG,
            local_path=Path('/tmp/test/local'),
        ),
        message_queue=KafkaFactory(KAFKA_CONFIG)
    )
    await service.ingestion_listener()


if __name__ == '__main__':
    asyncio.run(main())
