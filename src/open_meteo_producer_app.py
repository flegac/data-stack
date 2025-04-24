import datetime

from kafka_connector.kafka_factory import KafkaFactory
from measure_feature import MeasureQuery
from measure_feature.model.measure_query import Period
from measure_feature.model.sensor import MeasureType, Location
from measure_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG


def main():
    query = MeasureQuery(
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

    producer = KafkaFactory(KAFKA_CONFIG).producer(TEMPERATURES_TOPIC)
    for data in OpenMeteoMeasureReader(query).read_all():
        producer.write_batch(data)


if __name__ == '__main__':
    main()
