import asyncio
import datetime

from data_file_ingestion.config import TEMPERATURE_TOPIC
from measure_io.measure_query import Period, MeasureQuery
from measure_io.sensor import MeasureType, Location
from measure_io_open_meteo.open_meteo_measure_reader import OpenMeteoMeasureReader
from message_queue_kafka.kafka_factory import KafkaFactory
from src.config import KAFKA_CONFIG


async def main():
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

    producer = KafkaFactory(KAFKA_CONFIG).producer(TEMPERATURE_TOPIC)
    for data in OpenMeteoMeasureReader(query).read_all():
        await producer.write_batch(data)


if __name__ == '__main__':
    asyncio.run(main())
