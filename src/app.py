import datetime

from brocker_kafka.kafka_config import KafkaConfig
from brocker_kafka.kafka_consumer import KafkaConsumer
from brocker_kafka.kafka_producer import KafkaProducer
from measure_open_meteo.measure_open_meteo import MeasureOpenMeteo
from measure_repository import MeasureQuery
from measure_repository.model.measure_query import Period
from measure_repository.model.sensor import MeasureType, Location
from src.measure_serializer import MeasureSerializer

TEMPERATURES_TOPIC = KafkaConfig(
    broker_url='localhost:9092',
    topic='temperatures',
    group_id='temperature_group',
    serializer=MeasureSerializer()
)

if __name__ == '__main__':
    datasource = MeasureOpenMeteo()

    producer = KafkaProducer(TEMPERATURES_TOPIC)
    consumer = KafkaConsumer(TEMPERATURES_TOPIC)

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
