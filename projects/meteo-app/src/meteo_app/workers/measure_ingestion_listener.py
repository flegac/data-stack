from dataclasses import dataclass

from dependency_injector.wiring import Provide
from loguru import logger

from aa_common.mq.mq_backend import MQBackend
from meteo_domain.config import specific_measure_topic
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.ports.measure_repository import MeasureRepository


@dataclass
class MeasureIngestionListener:
    topic: str = "temperature"
    repo: MeasureRepository = Provide["repositories.measure_repository"]
    factory: MQBackend = Provide["repositories.mq_factory"]

    async def run(self):
        topic = specific_measure_topic(self.topic)

        consumer = self.factory.consumer(topic)
        await consumer.listen(self.measure_handler)

    async def measure_handler(self, measure: Measurement):
        logger.info(f"{measure}")
        await self.repo.save(measure)
