import datetime
from collections.abc import Iterable
from typing import override

import openmeteo_requests
import requests_cache
from meteo_domain.geo_sensor.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.geo_sensor.entities.telemetry.geo_sensor_series import GeoSensorSeries
from meteo_domain.geo_sensor.entities.telemetry.region_series import RegionSeries
from meteo_domain.geo_sensor.entities.telemetry.tagged_telemetry import TaggedTelemetry
from meteo_domain.geo_sensor.entities.telemetry.telemetry import (
    Telemetry,
)
from meteo_domain.geo_sensor.ports.tseries_repository import TSeriesRepository
from retry_requests import retry

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"


class OpenMeteoMeasureRepository(TSeriesRepository):
    @override
    async def init(self, reset: bool = False):
        pass

    @override
    async def save_batch(
        self, measures: Iterable[TaggedTelemetry], chunk_size: int = 100_000
    ):
        raise NotImplementedError

    @override
    def search(self, query: MeasureQuery = None) -> RegionSeries:
        if not (period := query.period):
            raise ValueError("period is required")

        cache_session = requests_cache.CachedSession(
            "/tmp/open-meteo/.cache", expire_after=-1
        )
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        series_list = []

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

            start_time = datetime.datetime.fromtimestamp(hourly.Time(), tz=datetime.UTC)
            interval = hourly.Interval()

            values = hourly.Variables(0).ValuesAsNumpy()
            times = [
                start_time + datetime.timedelta(seconds=i * interval)
                for i in range(len(values))
            ]

            measures = [
                Telemetry(
                    time=time,
                    value=value,
                )
                for time, value in zip(times, values, strict=False)
            ]

            series_list.append(
                GeoSensorSeries.from_measures(
                    sensor=sensor,
                    measures=measures,
                )
            )
        return RegionSeries(series=series_list)
