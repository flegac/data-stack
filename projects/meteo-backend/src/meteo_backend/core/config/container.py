from dependency_injector import containers, providers

from influxdb_connector.influxdb_config import InfluxDBConfig
from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from kafka_connector.kafka_config import KafkaConfig
from kafka_connector.kafka_connection import KafkaConnection
from kafka_message_queue.kafka_factory import KafkaMQBackend
from meteo_backend.core.config.settings import Settings
from meteo_domain.data_file.datafile_service import DataFileService
from meteo_domain.workspace.workspace_service import WorkspaceService
from redis_message_queue.redis_config import RedisConfig
from redis_message_queue.redis_connection import RedisConnection
from redis_message_queue.redis_factory import RedisMQBackend
from s3_connector.s3_config import S3Config
from s3_connector.s3_connection import S3Connection
from s3_file_repository.s3_file_repository import S3FileRepository
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.data_file import SqlDataFileRepository
from sql_meteo_adapters.workspace import SqlWorkspaceRepository


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

    sql_uow = providers.Singleton(SqlUnitOfWork, database_url)

    # DataFile Repository
    data_file_repository = providers.Singleton(SqlDataFileRepository, uow=sql_uow)

    # Workspace Repository
    ws_repository = providers.Singleton(SqlWorkspaceRepository, uow=sql_uow)
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
        InfluxDbTSeriesRepository,
        config=influxdb_config,
    )

    # configure redis
    redis_config = providers.Singleton(
        RedisConfig,
        host=settings.provided.REDIS_HOST,
        port=settings.provided.REDIS_PORT,
    )
    redis_connection = providers.Singleton(RedisConnection, redis_config)
    redis_mq_backend = providers.Singleton(
        RedisMQBackend,
        redis_connection,
    )

    # Configuration Kafka
    kafka_config = providers.Singleton(
        KafkaConfig,
        broker_url=settings.provided.KAFKA_BROKER_URL,
    )
    kafka_connection = providers.Singleton(KafkaConnection, kafka_config)

    kafka_mq_backend = providers.Singleton(
        KafkaMQBackend,
        kafka_connection,
    )

    # Service DataFile
    datafile_service = providers.Singleton(
        DataFileService,
        uow=sql_uow,
        mq_backend=redis_mq_backend,
        data_file_repository=data_file_repository,
        file_repository=file_repository,
        measure_repository=measure_repository,
    )

    # Service de Workspace
    ws_service = providers.Singleton(
        WorkspaceService,
        ws_repository=ws_repository,
        file_repository=file_repository,
        data_file_repository=data_file_repository,
    )
