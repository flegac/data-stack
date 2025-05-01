import asyncio

from measure_repository_influxdb.measure_writer_influxdb import InfluxDbMeasureWriter
from message_queue_kafka.kafka_factory import KafkaFactory
from meteo_measures.config import TEMPERATURE_TOPIC
from src.config import KAFKA_CONFIG, INFLUX_DB_CONFIG


async def main():
    influx_db_writer = InfluxDbMeasureWriter(INFLUX_DB_CONFIG)

    async def handler(measure):
        print(measure)
        influx_db_writer.write(measure)

    factory = KafkaFactory(KAFKA_CONFIG)
    consumer = factory.consumer(TEMPERATURE_TOPIC)
    await consumer.listen(handler)


if __name__ == '__main__':
    asyncio.run(main())
