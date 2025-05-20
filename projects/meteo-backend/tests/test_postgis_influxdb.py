import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import TestCase

import cv2
from easy_kit.timing import setup_timing, time_func
from influxdb_connector.influxdb_config import InfluxDBConfig
from location_api_geopy.location_api_geopy import GeopyLocationAPI
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from meteo_domain.core.logger import logger
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork
from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor
from meteo_domain.geo_sensor.entities.location.location import Location
from meteo_domain.geo_sensor.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.geo_sensor.entities.times.period import Period
from meteo_domain.geo_sensor.heatmap_service import HeatmapService
from meteo_domain.geo_sensor.location_service import LocationService
from meteo_domain.geo_sensor.ports.tseries_repository import TSeriesRepository
from meteo_domain.geo_sensor.sensor_service import SensorService
from unit_of_work_sql.sql_unit_of_work import SqlUnitOfWork

CENTER = Location(name="Paris", latitude=48.8566, longitude=2.3522)
RADIUS_KM = 50

SENSOR_NUMBER = 200
batch_size = 10_000


class TestPostgisInfluxdb(TestCase):
    def test_it(self):
        setup_timing()
        loc_service = LocationService(GeopyLocationAPI())
        database_url = (
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
        uow = SqlUnitOfWork(database_url)

        measures = InfluxDbTSeriesRepository(
            InfluxDBConfig(
                url="http://localhost:8086",
                token="server-token",
                org="meteo-org",
                bucket="meteo-data",
            )
        )
        asyncio.run(
            weather_workflow(
                uow,
                measures,
                loc_service,
            )
        )


@time_func
def measure_generator(sensors: list[GeoSensor]):
    sensor_service = SensorService()

    start = datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    period = Period.from_duration(start, timedelta(days=20))

    for sensor in sensors:
        yield from sensor_service.fake_measurements(sensor, period, 20 * 23)


async def weather_workflow(
    uow: SqlUnitOfWork,
    temperature_repo: TSeriesRepository,
    loc_service: LocationService,
):
    await uow.connection.kill_all_connections()
    await uow.sensors().drop_table()
    await uow.sensors().create_table()

    sensors = await populate_sensors(loc_service, uow)

    logger.info("generate telemetries ...")
    telemetries = measure_generator(sensors)
    logger.info("telemetries generated !")

    await temperature_repo.init(reset=True)
    await temperature_repo.save_batch(telemetries, chunk_size=batch_size)

    # Test de recherche spatiale
    async with uow.transaction():
        nearby_sensors = await uow.sensors().find_in_radius(CENTER, RADIUS_KM)
    logger.info(
        f"\nCapteurs trouvés dans un rayon de {RADIUS_KM}km: {len(nearby_sensors)}"
    )
    assert len(nearby_sensors) > 0

    if nearby_sensors:
        now = datetime.now(UTC)
        region_series = temperature_repo.search(
            MeasureQuery(
                sources=nearby_sensors,
                period=Period.from_duration(
                    now.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    timedelta(days=1),
                ),
            )
        )

        target_path = Path.cwd() / "output"
        target_path.mkdir(parents=True, exist_ok=True)

        for idx, measures in enumerate(region_series.iter_timeline()):
            heatmap_service = HeatmapService()
            heatmap = heatmap_service.compute_heatmap(measures, min_distance=0.0)
            cv2.imwrite(str(target_path / f"heatmap_{idx}.png"), heatmap)


async def populate_sensors(
    loc_service: LocationService, uow: UnitOfWork
) -> list[GeoSensor]:
    locations = [
        *[
            loc_service.random_in_radius(CENTER, RADIUS_KM)
            for _ in range(SENSOR_NUMBER)
        ],
        # *loc_service.generate_french_locations(SENSOR_NUMBER),
    ]
    # Création des capteurs
    sensors = [
        GeoSensor(
            uid=f"FR{idx:05d}",
            measure_type="temperature",
            location=location,
        )
        for idx, location in enumerate(locations)
    ]
    async with uow.transaction():
        await uow.sensors().save(sensors)
    return sensors
