from collections.abc import Generator, Iterable
from typing import Any, override

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measure_series import MeasureSeries
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.ports.measure_repository import MeasureRepository

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


class OpenMeteoMeasureRepository(MeasureRepository):

    @override
    async def init(self, reset: bool = False):
        pass

    @override
    async def save_batch(
        self, measures: Iterable[Measurement], chunk_size: int = 100_000
    ):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery = None) -> Generator[MeasureSeries, Any]:
        if not (period := query.period):
            raise ValueError("period is required")

        cache_session = requests_cache.CachedSession(
            "/tmp/open-meteo/.cache", expire_after=-1
        )
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        for sensor in query.sources:
            location = sensor.location
            measure_type = sensor.measure_type
            responses = openmeteo.weather_api(
                OPEN_METEO_URL,
                params={
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": period.start.date().isoformat(),
                    "end_date": period.end.date().isoformat(),
                    "hourly": measure_type,
                },
            )

            location_0 = responses[0]
            hourly = location_0.Hourly()
            yield MeasureSeries(
                sensor=sensor,
                measures=pd.DataFrame(
                    data={
                        "time": pd.date_range(
                            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                            freq=pd.Timedelta(seconds=hourly.Interval()),
                            inclusive="left",
                        ),
                        "value": hourly.Variables(0).ValuesAsNumpy(),
                    }
                ),
            )
