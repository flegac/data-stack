from pathlib import Path

from dependency_injector import containers, providers

from file_repository_s3.s3_config import S3Config
from measure_repository_influxdb.influxdb_config import InfluxDBConfig
from message_queue_kafka.kafka_config import KafkaConfig


class Config(containers.DeclarativeContainer):
    database_url = providers.Object('postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase')

    s3 = providers.Factory(
        S3Config,
        endpoint='http://localhost:9000',
        access_key='admin',
        secret_key='adminpassword'
    )
    local_path = providers.Object(Path('/tmp/test/local'))

    kafka = providers.Factory(
        KafkaConfig,
        broker_url='localhost:9092',
        group_id='meteo_group'
    )

    influx_db = providers.Factory(
        InfluxDBConfig,
        url='http://localhost:8086',
        org='myorg',
        token='SDha-behzzOhZyZ1v1xfnjKtDhWbk_uZDuLyUJvHXYQSGSJkwXBVFj9F8dhnPMZoXLkRRuih_E5gJfJ3d3sdBw==',
        bucket='meteo-data'
    )
