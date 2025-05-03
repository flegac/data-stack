import asyncio
import datetime

from measure_repository_openmeteo.open_meteo_measure_repository import (
    OpenMeteoMeasureRepository,
)
from message_queue_kafka.kafka_factory import KafkaMQFactory
from meteo_measures.config import specific_measure_topic
from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.period import Period

from meteo_app.config import KAFKA_CONFIG


async def main():
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
    producer = KafkaMQFactory(KAFKA_CONFIG).producer(topic)
    for data in repo.search(query):
        await producer.write_batch(data)


if __name__ == "__main__":
    asyncio.run(main())
