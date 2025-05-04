from message_queue.mq_topic import MQTopic

from meteo_domain.entities.data_file_serializer import DataFileSerializer
from meteo_domain.entities.measures.measure_serializer import MeasureSerializer


def specific_measure_topic(name: str):
    return MQTopic(topic=f"{name}.topic", serializer=MeasureSerializer())


MEASURE_TOPIC = specific_measure_topic("measure")

TEMPERATURE_TOPIC = MQTopic(topic="temperature.topic", serializer=MeasureSerializer())

DATAFILE_INGESTION_TOPIC = MQTopic(
    topic="DataFile.ingestion.topic", serializer=DataFileSerializer()
)

DATAFILE_ERROR_TOPIC = MQTopic(
    topic="DataFile.error.topic", serializer=DataFileSerializer()
)
