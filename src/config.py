from broker_api.broker_topic import BrokerTopic
from broker_kafka.kafka_config import KafkaConfig
from broker_kafka.kafka_factory import KafkaFactory
from measure_influxdb.influxdb_config import InfluxDBConfig
from src.measure_serializer import MeasureSerializer

INFLUX_DB_CONFIG = InfluxDBConfig(
    url="http://localhost:8086",
    org="myorg",
    token='k5OmUjRQ0R-unlkmdwoGIV4aYNSqUyfG3uY2I7y1VqIQy5jcE_ErXYQ4b-Epq8BzrmrUwIw1a0zIZV6FCqgd8g==',
    bucket="meteo-data"
)
KAFKA_CONFIG = KafkaConfig(
    broker_url='localhost:9092',
    group_id='temperature_group'
)

TEMPERATURES_TOPIC = BrokerTopic(
    topic='temperatures',
    serializer=MeasureSerializer()
)
