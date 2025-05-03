from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository
from dependency_injector import containers, providers
from file_repository_s3.s3_file_repository import S3FileRepository
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from message_queue_kafka.kafka_factory import KafkaMQFactory

from meteo_app.wires.config import Config


# pylint: disable=too-few-public-methods
class Repositories(containers.DeclarativeContainer):
    config = providers.Container(Config)
    mq_factory = providers.Singleton(KafkaMQFactory, config=config.kafka)
    data_file_repository = providers.Singleton(
        PgDataFileRepository, database_url=config.database_url
    )

    file_repository = providers.Singleton(
        S3FileRepository, config=config.s3, local_path=config.local_path
    )

    measure_repository = providers.Singleton(
        InfluxDbMeasureRepository, config=config.influx_db
    )
