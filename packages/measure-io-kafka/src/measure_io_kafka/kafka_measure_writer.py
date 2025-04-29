from abc import abstractmethod

from message_queue_kafka.kafka_producer import KafkaProducer
from measure_io.measure import MeasureSeries, Measure
from measure_io.measure_writer import MeasureWriter


class KafkaMeasureWriter(MeasureWriter):
    def __init__(self, producer: KafkaProducer[Measure]):
        self.producer = producer

    @abstractmethod
    def write(self, measure: Measure):
        self.producer.write_single(measure)

    @abstractmethod
    def write_batch(self, measures: MeasureSeries):
        self.producer.write_batch(measures)
