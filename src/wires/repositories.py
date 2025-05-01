from dependency_injector import containers, providers

from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository
from file_repository_s3.s3_file_repository import S3FileRepository
from measure_repository_influxdb.influxdb_measure_repository import InfluxDbMeasureRepository
from message_queue_kafka.kafka_factory import KafkaFactory
from wires.config import Config


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Container(Config)

    data_file_repository = providers.Singleton(
        PgDataFileRepository,
        database_url=config.database_url
    )
    file_repository = providers.Singleton(
        S3FileRepository,
        config=config.s3,
        local_path=config.local_path,
    )
    mq_factory = providers.Singleton(
        KafkaFactory,
        config=config.kafka,
    )

    measure_repository = providers.Singleton(
        InfluxDbMeasureRepository,
        config=config.influx_db
    )
