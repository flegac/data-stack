import asyncio
import datetime

from kafka_connector.kafka_connection import KafkaConnection
from kafka_message_queue import KafkaMQBackend
from meteo_app.config import KAFKA_CONFIG
from meteo_domain.config import specific_measure_topic
from meteo_domain.entities.geo_spatial.location import Location
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.temporal.period import Period
from openmeteo_measure_repository import (
    OpenMeteoMeasureRepository,
)


async def main():
    kafka_connection = KafkaConnection(KAFKA_CONFIG)
    repo = OpenMeteoMeasureRepository()
    variable = "temperature"

    query = MeasureQuery(
        measure_type=variable,
        period=Period(
            start=datetime.datetime(2025, 4, 6, tzinfo=datetime.UTC),
            end=datetime.datetime(2025, 4, 13, tzinfo=datetime.UTC),
        ),
        location=Location(latitude=43.6043, longitude=1.4437),
    )
    topic = specific_measure_topic(variable)
    producer = KafkaMQBackend(kafka_connection).producer(topic)
    for data in repo.search(query):
        await producer.write_batch(data)


if __name__ == "__main__":
    asyncio.run(main())
