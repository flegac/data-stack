from dataclasses import dataclass

from measure_repository.model.location import Location
from measure_repository.model.measure_type import MeasureType
from measure_repository.model.period import Period


@dataclass
class MeasureQuery:
    sensor_id: str | None = None
    period: Period | None = None
    location: Location | None = None
    measure_type: MeasureType | None = None
