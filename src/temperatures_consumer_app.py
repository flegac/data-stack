import asyncio

from kafka_connector.kafka_factory import KafkaFactory
from measure_io_influxdb.measure_writer_influxdb import InfluxDbMeasureWriter
from src.config import TEMPERATURES_TOPIC, KAFKA_CONFIG, INFLUX_DB_CONFIG


async def main():
    influx_db_writer = InfluxDbMeasureWriter(INFLUX_DB_CONFIG)

    async def measure_influxdb_write(measure):
        print(measure)
        influx_db_writer.write(measure)

    factory = KafkaFactory(KAFKA_CONFIG)
    consumer = factory.consumer(TEMPERATURES_TOPIC)
    await consumer.listen(measure_influxdb_write)


if __name__ == '__main__':
    asyncio.run(main())
