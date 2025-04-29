import asyncio
from pathlib import Path

from loguru import logger

from config import POSTGRE_URl, S3_CONFIG, KAFKA_CONFIG, INGESTION_TOPIC
from data_file_ingestion.data_file_ingestion_service import DataFileIngestionService
from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository
from file_repository_s3.s3_file_repository import S3FileRepository
from message_queue_kafka.kafka_factory import KafkaFactory


async def main():
    factory = KafkaFactory(KAFKA_CONFIG)

    service = DataFileIngestionService(
        data_file_repository=PgDataFileRepository(POSTGRE_URl),
        file_repository=S3FileRepository(
            config=S3_CONFIG,
            local_path=Path('/tmp/test/local'),
        ),
        producer=factory.producer(INGESTION_TOPIC)
    )

    item = await service.upload_file('toto', Path(__file__))
    logger.debug(f'{item}')

    # TODO: use as a callback in KafkaConsumer.listen()
    await service.ingest_file(item)


if __name__ == '__main__':
    asyncio.run(main())
