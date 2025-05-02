from dataclasses import dataclass

from dependency_injector.wiring import Provide
from message_queue import MQFactory
from meteo_measures.config import specific_measure_topic
from meteo_measures.domain.entities.measures.measure import Measure
from meteo_measures.domain.ports.measure_repository import MeasureRepository


@dataclass
class MeasureIngestionListener:
    topic: str = "temperature"
    repo: MeasureRepository = Provide["repositories.measure_repository"]
    factory: MQFactory = Provide["repositories.mq_factory"]

    async def run(self):
        topic = specific_measure_topic(self.topic)

        consumer = self.factory.consumer(topic)
        await consumer.listen(self.measure_handler)

    async def measure_handler(self, measure: Measure):
        print(measure)
        await self.repo.save(measure)
