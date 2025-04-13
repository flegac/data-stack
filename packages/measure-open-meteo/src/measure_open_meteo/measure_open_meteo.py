import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from measure_repository import Measure, MeasureQuery, MeasureSeries
from measure_repository.measure_repository import MeasureRepository
from measure_repository.model.sensor import Sensor, Location, MeasureType

OPEN_METEO_URL = 'https://archive-api.open-meteo.com/v1/archive'


class MeasureOpenMeteo(MeasureRepository):

    def write(self, measure: Measure):
        raise NotImplementedError('could not write to Open-Meteo database')

    def write_batch(self, measures: MeasureSeries):
        raise NotImplementedError('could not write to Open-Meteo database')

    def search(self, query: MeasureQuery):
        if not (measure_type := query.measure_type):
            raise ValueError('measure_type is required')
        if not (location := query.location):
            raise ValueError('location is required')
        if not (period := query.period):
            raise ValueError('period is required')

        measure_type_binding = _measure_type_mapping(measure_type)

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
                'hourly': measure_type_binding
            }
        )

        location_0 = responses[0]
        hourly = location_0.Hourly()

        return MeasureSeries(
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


def _measure_type_mapping(measure_type: MeasureType):
    match measure_type:
        case MeasureType.TEMPERATURE:
            return "temperature_2m"
        case MeasureType.HUMIDITY:
            return "relative_humidity"
        case MeasureType.PRESSURE:
            return "pressure_msl"
        case MeasureType.WIND_SPEED:
            return "wind_speed_10m"
        case MeasureType.RAIN:
            return "precipitation"

    raise ValueError(f'measure_type {measure_type} is not supported')
