from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository
from dependency_injector import containers, providers
from file_repository_s3.s3_file_repository import S3FileRepository
from influxdb_connector.influxdb_config import InfluxDBConfig
from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.kafka_connection import KafkaConnection
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from message_queue_kafka.kafka_factory import KafkaMQBackend
from meteo_domain.services.data_file_ingestion_service import DataFileIngestionService
from meteo_domain.services.data_file_messaging_service import DataFileMessagingService
from meteo_domain.services.data_file_upload_service import DataFileUploadService
from s3_connector.s3_config import S3Config
from s3_connector.s3_connection import S3Connection

from meteo_backend.core.config.settings import Settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = providers.Singleton(Settings)

    # Configuration S3
    s3_config = providers.Singleton(
        S3Config,
        access_key=settings.provided.S3_ACCESS_KEY,
        secret_key=settings.provided.S3_SECRET_KEY,
        region=settings.provided.S3_REGION,
        endpoint=settings.provided.S3_ENDPOINT,
    )

    s3_connection = providers.Singleton(S3Connection, s3_config)

    # File Repository
    file_repository = providers.Singleton(
        S3FileRepository,
        local_path=settings.provided.LOCAL_STORAGE_PATH,
        bucket=settings.provided.S3_BUCKET,
        connection=s3_connection,
    )

    # PostgreSQL URL construction
    database_url = providers.Factory(
        lambda s: f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}",
        settings,
    )

    # DataFile Repository
    data_file_repository = providers.Singleton(
        PgDataFileRepository, database_url=database_url
    )

    # Configuration InfluxDB (à ajouter dans Settings aussi)
    influxdb_config = providers.Singleton(
        InfluxDBConfig,
        url=settings.provided.INFLUXDB_URL,
        token=settings.provided.INFLUXDB_TOKEN,
        org=settings.provided.INFLUXDB_ORG,
        bucket=settings.provided.INFLUXDB_BUCKET,
    )

    # Measure Repository
    measure_repository = providers.Singleton(
        InfluxDbMeasureRepository,
        config=influxdb_config,
    )

    # Configuration Kafka
    kafka_config = providers.Singleton(
        KafkaConfig,
        broker_url=settings.provided.KAFKA_BROKER_URL,
    )
    kafka_connection = providers.Singleton(KafkaConnection, kafka_config)

    # Message Queue Factory
    mq_factory = providers.Singleton(
        KafkaMQBackend,
        kafka_connection,
    )

    # Service de Messaging
    messaging_service = providers.Singleton(
        DataFileMessagingService,
        data_file_repository=data_file_repository,
        mq_factory=mq_factory,
    )

    # Service d'Upload
    file_service = providers.Singleton(
        DataFileUploadService,
        messaging=messaging_service,
        file_repository=file_repository,
        data_file_repository=data_file_repository,
    )

    # Service d'ingestion
    ingestion_service = providers.Singleton(
        DataFileIngestionService,
        messaging=messaging_service,
        data_file_repository=data_file_repository,
        file_repository=file_repository,
        measure_repository=measure_repository,
    )
