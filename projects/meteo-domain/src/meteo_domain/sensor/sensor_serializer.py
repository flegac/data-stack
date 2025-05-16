import datetime
from dataclasses import asdict

from meteo_domain.core.message_queue.serializer import Serializer
from meteo_domain.sensor.entities.sensor import Sensor


class SensorSerializer(Serializer[Sensor, dict]):
    def serialize(self, message: Sensor) -> dict:
        raw = asdict(message)
        raw["creation_date"] = message.creation_date.isoformat()
        raw["last_update_date"] = message.last_update_date.isoformat()
        return raw

    def deserialize(self, raw: dict) -> Sensor:
        for date_key in ["creation_date", "last_update_date"]:
            raw[date_key] = datetime.datetime.fromisoformat(raw[date_key])
        return Sensor(**raw)
