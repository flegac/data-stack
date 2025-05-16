from dependency_injector import containers, providers

from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from kafka_connector.kafka_connection import KafkaConnection
from kafka_message_queue.kafka_factory import KafkaMQBackend
from meteo_app.wires.config import Config
from s3_connector.s3_connection import S3Connection
from s3_file_repository.s3_file_repository import S3FileRepository
from sql_connector.sql_connection import SqlConnection
from sql_meteo_adapters.repositories import (
    SqlWorkspaceRepository,
    SqlDataFileRepository,
)


# pylint: disable=too-few-public-methods
class Repositories(containers.DeclarativeContainer):
    config = providers.Container(Config)

    kafka_connection = providers.Singleton(KafkaConnection, config=config.kafka)

    mq_factory = providers.Singleton(KafkaMQBackend, connection=kafka_connection)

    ws_repository = providers.Singleton(
        SqlWorkspaceRepository, database_url=config.database_url
    )

    s3_connection = providers.Singleton(S3Connection, config=config.s3)

    file_repository = providers.Singleton(
        S3FileRepository, connection=s3_connection, local_path=config.local_path
    )

    measure_repository = providers.Singleton(
        InfluxDbMeasureRepository, config=config.influx_db
    )

    sql_connection = providers.Singleton(SqlConnection, config.database_url)

    data_file_repository = providers.Singleton(
        SqlDataFileRepository, connection=sql_connection
    )
