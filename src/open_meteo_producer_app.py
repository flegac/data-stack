import datetime

from broker_kafka.kafka_factory import KafkaFactory
from measure_open_meteo.measure_open_meteo import MeasureOpenMeteo
from measure_repository import MeasureQuery
from measure_repository.model.measure_query import Period
from measure_repository.model.sensor import MeasureType, Location
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG


def main():
    producer = KafkaFactory(KAFKA_CONFIG).producer(TEMPERATURES_TOPIC)
    data = MeasureOpenMeteo().search(
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


if __name__ == '__main__':
    main()
