from typing import Generator, Any, override, Iterable

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from meteo_measures.domain.entities.measure_query import MeasureQuery
from meteo_measures.domain.entities.measures.location import Location
from meteo_measures.domain.entities.measures.measure import Measure
from meteo_measures.domain.entities.measures.measure_series import MeasureSeries
from meteo_measures.domain.entities.measures.sensor import Sensor
from meteo_measures.domain.ports.measure_repository import MeasureRepository

OPEN_METEO_URL = 'https://archive-api.open-meteo.com/v1/archive'


class OpenMeteoMeasureRepository(MeasureRepository):
    @override
    async def save_batch(self, measures: Iterable[Measure]):
        raise NotImplementedError

    @override
    async def save(self, measure: Measure):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery) -> Generator[MeasureSeries, Any, None]:
        if not (measure_type := query.measure_type):
            raise ValueError('measure_type is required')
        if not (location := query.location):
            raise ValueError('location is required')
        if not (period := query.period):
            raise ValueError('period is required')

        cache_session = requests_cache.CachedSession('/tmp/open-meteo/.cache', expire_after=-1)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        responses = openmeteo.weather_api(
            OPEN_METEO_URL,
            params={
                'latitude': location.latitude,
                'longitude': location.longitude,
                'start_date': period.start.date().isoformat(),
                'end_date': period.end.date().isoformat(),
                'hourly': measure_type
            }
        )

        location_0 = responses[0]
        hourly = location_0.Hourly()

        yield MeasureSeries(
            sensor=Sensor(
                id='OpenMeteo',
                type=query.measure_type,
                location=Location(
                    latitude=location_0.Latitude(),
                    longitude=location_0.Longitude(),
                    altitude=location_0.Elevation()
                )
            ),
            measures=pd.DataFrame(data={
                "datetime": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                ),
                "value": hourly.Variables(0).ValuesAsNumpy()
            })
        )
