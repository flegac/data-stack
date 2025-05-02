from pathlib import Path

from dependency_injector import containers, providers
from file_repository_s3.s3_config import S3Config
from measure_repository_influxdb.influxdb_config import InfluxDBConfig
from message_queue_kafka.kafka_config import KafkaConfig

INI_FILE = Path(__file__).parent / "config.ini"


class Config(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    kafka = providers.Singleton(
        KafkaConfig, config.kafka.broker_url, config.kafka.group_id
    )

    database_url = config.database.url
    local_path = config.local.path

    s3 = providers.Singleton(
        S3Config,
        endpoint=config.s3.endpoint,
        access_key=config.s3.access_key,
        secret_key=config.s3.secret_key,
    )
    influx_db = providers.Factory(
        InfluxDBConfig,
        url=config.influxdb.url,
        org=config.influxdb.org,
        token=config.influxdb.token,
        bucket=config.influxdb.bucket,
    )
