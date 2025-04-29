from data_file_repository.data_file_serializer import DataFileSerializer
from file_repository_s3.s3_config import S3Config
from measure_io.measure_serializer import MeasureSerializer
from measure_io_influxdb.influxdb_config import InfluxDBConfig
from message_queue.mq_topic import MQTopic
from message_queue_kafka.kafka_config import KafkaConfig

POSTGRE_URl = 'postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase'

S3_CONFIG = S3Config(
    endpoint='http://localhost:9000',
    access_key='admin',
    secret_key='adminpassword'
)

INFLUX_DB_CONFIG = InfluxDBConfig(
    url='http://localhost:8086',
    org='myorg',
    token='k5OmUjRQ0R-unlkmdwoGIV4aYNSqUyfG3uY2I7y1VqIQy5jcE_ErXYQ4b-Epq8BzrmrUwIw1a0zIZV6FCqgd8g==',
    bucket='meteo-data'
)
KAFKA_CONFIG = KafkaConfig(
    broker_url='localhost:9092',
    group_id='temperature_group'
)

TEMPERATURE_TOPIC = MQTopic(
    topic='TEMPERATURE_TOPIC',
    serializer=MeasureSerializer()
)
INGESTION_TOPIC = MQTopic(
    topic='INGESTION_TOPIC',
    serializer=DataFileSerializer()
)
