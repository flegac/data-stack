from abc import ABC, abstractmethod

from measure_repository.model.sensor import Sensor, SensorId


class SensorRepository(ABC):
    @abstractmethod
    def save(self, sensor: Sensor):
        ...

    @abstractmethod
    def load_by_id(self, sensor_id: SensorId) -> Sensor:
        ...
