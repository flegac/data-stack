from typing import override, Generator, Any

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from measure_repository_openmeteo.config import OPEN_METEO_URL
from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.measure_series import MeasureSeries
from meteo_measures.domain.entities.measures.sensor import Sensor
from meteo_measures.domain.ports.measure_reader import MeasureReader


class OpenMeteoMeasureReader(MeasureReader):
    def __init__(self, query: MeasureQuery):
        self.query = query

    @override
    def read_all(self) -> Generator[MeasureSeries, Any, None]:

