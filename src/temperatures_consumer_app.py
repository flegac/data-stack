import asyncio

from broker_kafka.kafka_factory import KafkaFactory
from measure_influxdb.measure_influxdb import MeasureInfluxDb
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG, INFLUX_DB_CONFIG


async def main():
    measure_influxdb = MeasureInfluxDb(INFLUX_DB_CONFIG)

    async def measure_influxdb_write(measure):
        print(measure)
        measure_influxdb.write(measure)

    factory = KafkaFactory(KAFKA_CONFIG)
    consumer = factory.consumer(TEMPERATURES_TOPIC)
    await consumer.listen(measure_influxdb_write)


if __name__ == '__main__':
    asyncio.run(main())
