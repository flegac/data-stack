from data_file_repository.data_file_serializer import DataFileSerializer
from measure_io.measure_serializer import MeasureSerializer
from message_queue.mq_topic import MQTopic

MEASURE_TOPIC = MQTopic(
    topic='measure.topic',
    serializer=MeasureSerializer()
)

TEMPERATURE_TOPIC = MQTopic(
    topic='temperature.topic',
    serializer=MeasureSerializer()
)

DATAFILE_INGESTION_TOPIC = MQTopic(
    topic='DataFile.ingestion.topic',
    serializer=DataFileSerializer()
)

DATAFILE_ERROR_TOPIC = MQTopic(
    topic='DataFile.error.topic',
    serializer=DataFileSerializer()
)
