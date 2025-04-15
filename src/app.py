import datetime

from broker_api.broker_topic import BrokerTopic
from broker_kafka.kafka_config import KafkaConfig
from broker_kafka.kafka_factory import KafkaFactory
from measure_open_meteo.measure_open_meteo import MeasureOpenMeteo
from measure_repository import MeasureQuery
from measure_repository.model.measure_query import Period
from measure_repository.model.sensor import MeasureType, Location
from src.measure_serializer import MeasureSerializer

KAFKA_FACTORY = KafkaFactory(KafkaConfig(
    broker_url='localhost:9092',
    group_id='temperature_group'
))

TEMPERATURES_TOPIC = BrokerTopic(
    topic='temperatures',
    serializer=MeasureSerializer()
)

if __name__ == '__main__':
    datasource = MeasureOpenMeteo()

    producer = KAFKA_FACTORY.producer(TEMPERATURES_TOPIC)
    consumer = KAFKA_FACTORY.consumer(TEMPERATURES_TOPIC)

    data = datasource.search(
        MeasureQuery(
            measure_type=MeasureType.TEMPERATURE,
            period=Period(
                start=datetime.datetime(2025, 4, 6, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 4, 13, tzinfo=datetime.timezone.utc)
            ),
            location=Location(
                latitude=43.6043,
                longitude=1.4437
            ),
        )
    )
    producer.write_batch(data)

    # Consume messages
    consumer.listen(lambda x: print(x))
