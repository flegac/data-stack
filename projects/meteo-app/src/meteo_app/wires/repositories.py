from dependency_injector import containers, providers

from file_repository_s3.s3_file_repository import S3FileRepository
from kafka_connector.kafka_connection import KafkaConnection
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from message_queue_kafka.kafka_factory import KafkaMQBackend
from meteo_app.wires.config import Config
from s3_connector.s3_connection import S3Connection
from unit_of_work_sql.repositories.data_file import SqlDataFileRepository
from unit_of_work_sql.repositories.workspace import SqlWorkspaceRepository
from unit_of_work_sql.sql_unit_of_work import SqlUnitOfWork


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
        InfluxDbTSeriesRepository, config=config.influx_db
    )

    sql_uow = providers.Singleton(SqlUnitOfWork, config.database_url)

    data_file_repository = providers.Singleton(SqlDataFileRepository, uow=sql_uow)
