import asyncio

from kafka_connector.kafka_factory import KafkaFactory
from influxdb_connector.measure_influxdb import InfluxDbMeasureRepository
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG, INFLUX_DB_CONFIG


async def main():
    measure_influxdb = InfluxDbMeasureRepository(INFLUX_DB_CONFIG)

    async def measure_influxdb_write(measure):
        print(measure)
        measure_influxdb.write(measure)

    factory = KafkaFactory(KAFKA_CONFIG)
    consumer = factory.consumer(TEMPERATURES_TOPIC)
    await consumer.listen(measure_influxdb_write)


if __name__ == '__main__':
    asyncio.run(main())
