from pathlib import Path

from meteo_domain.core.message_queue.mq_topic import MQTopic
from meteo_domain.serializers.datafile_serializer import DataFileSerializer
from meteo_domain.serializers.measurement_serializer import MeasurementSerializer

DATASET_ROOT_PATH = Path.home() / "Documents" / "Data" / "Datasets"
LOCAL_STORAGE_PATH = Path("/tmp/meteo-files")
EXPORT_PATH = LOCAL_STORAGE_PATH / "exports"
LOCAL_TEST_PATH = LOCAL_STORAGE_PATH / "tests"


def specific_measure_topic(name: str):
    return MQTopic(topic=f"{name}.topic", serializer=MeasurementSerializer())


MEASURE_TOPIC = specific_measure_topic("measure")
TEMPERATURE_TOPIC = specific_measure_topic("temperature")

DATAFILE_INGESTION_TOPIC = MQTopic(
    topic="DataFile.ingestion.topic", serializer=DataFileSerializer()
)

DATAFILE_ERROR_TOPIC = MQTopic(
    topic="DataFile.error.topic", serializer=DataFileSerializer()
)
