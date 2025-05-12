from aa_common.mq.mq_topic import MQTopic

from meteo_domain.data_file.datafile_serializer import DataFileSerializer
from meteo_domain.temporal_series.measurement_serializer import MeasurementSerializer


def specific_measure_topic(name: str):
    return MQTopic(topic=f"{name}.topic", serializer=MeasurementSerializer())


MEASURE_TOPIC = specific_measure_topic("measure")

TEMPERATURE_TOPIC = MQTopic(
    topic="temperature.topic", serializer=MeasurementSerializer()
)

DATAFILE_INGESTION_TOPIC = MQTopic(
    topic="DataFile.ingestion.topic", serializer=DataFileSerializer()
)

DATAFILE_ERROR_TOPIC = MQTopic(
    topic="DataFile.error.topic", serializer=DataFileSerializer()
)
