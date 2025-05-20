import datetime
from dataclasses import asdict

from meteo_domain.core.message_queue.serializer import Serializer
from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor


class SensorSerializer(Serializer[GeoSensor, dict]):
    def serialize(self, message: GeoSensor) -> dict:
        raw = asdict(message)
        raw["creation_date"] = message.creation_date.isoformat()
        raw["last_update_date"] = message.last_update_date.isoformat()
        return raw

    def deserialize(self, raw: dict) -> GeoSensor:
        for date_key in ["creation_date", "last_update_date"]:
            raw[date_key] = datetime.datetime.fromisoformat(raw[date_key])
        return GeoSensor(**raw)
