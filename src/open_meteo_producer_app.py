import datetime

from kafka_connector.kafka_factory import KafkaFactory
from measure_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader
from measure_feature import MeasureQuery
from measure_feature.model.measure_query import Period
from measure_feature.model.sensor import MeasureType, Location
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG


def main():
    producer = KafkaFactory(KAFKA_CONFIG).producer(TEMPERATURES_TOPIC)
    data = OpenMeteoMeasureReader().search(
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
