from influxdb_connector.influxdb_config import InfluxDBConfig
from kafka_connector.kafka_config import KafkaConfig
from s3_connector.s3_config import S3Config

POSTGRE_URL = "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"

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

KAFKA_CONFIG = KafkaConfig(broker_url="localhost:9092")
