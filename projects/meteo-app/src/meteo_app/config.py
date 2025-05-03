from file_repository_s3.s3_config import S3Config
from measure_repository_influxdb.influxdb_config import InfluxDBConfig
from message_queue_kafka.kafka_config import KafkaConfig

POSTGRE_URL = "postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase"

S3_CONFIG = S3Config(
    endpoint="http://localhost:9000",
    access_key="admin",
    secret_key="adminpassword",
)

INFLUX_DB_CONFIG = InfluxDBConfig(
    url="http://localhost:8086",
    org="myorg",
    token="server-token",
    bucket="meteo-data",
)

KAFKA_CONFIG = KafkaConfig(broker_url="localhost:9092", group_id="meteo-group")
