from dependency_injector import containers, providers
from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from kafka_message_queue.kafka_factory import KafkaMQBackend
from pg_meteo_adapters.data_file_repository import PgDataFileRepository
from pg_meteo_adapters.ws_repository import PgWorkspaceRepository
from s3_file_repository.s3_file_repository import S3FileRepository

from meteo_app.wires.config import Config


# pylint: disable=too-few-public-methods
class Repositories(containers.DeclarativeContainer):
    config = providers.Container(Config)
    mq_factory = providers.Singleton(KafkaMQBackend, config=config.kafka)

    ws_repository = providers.Singleton(
        PgWorkspaceRepository, database_url=config.database_url
    )

    data_file_repository = providers.Singleton(
        PgDataFileRepository, database_url=config.database_url
    )

    file_repository = providers.Singleton(
        S3FileRepository, config=config.s3, local_path=config.local_path
    )

    measure_repository = providers.Singleton(
        InfluxDbMeasureRepository, config=config.influx_db
    )
