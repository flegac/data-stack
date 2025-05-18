import asyncio
from datetime import UTC, datetime, timedelta
from unittest import TestCase

import cv2

from influxdb_connector.influxdb_config import InfluxDBConfig
from location_api_geopy.location_api_geopy import GeopyLocationAPI
from measure_repository_influxdb.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork
from meteo_domain.measurement.entities.measure_query import (
    MeasureQuery,
)
from meteo_domain.measurement.entities.period import Period
from meteo_domain.measurement.entities.sensor.location import Location
from meteo_domain.measurement.entities.sensor.sensor import Sensor
from meteo_domain.measurement.heatmap_service import HeatmapService
from meteo_domain.measurement.location_service import LocationService
from meteo_domain.measurement.ports.tseries_repository import TSeriesRepository
from meteo_domain.measurement.sensor_service import SensorService
from unit_of_work_sql.sql_unit_of_work import SqlUnitOfWork

CENTER = Location(name="Paris", latitude=48.8566, longitude=2.3522)
RADIUS_KM = 50

SENSOR_NUMBER = 1_000
MEASUREMENT_PER_SENSOR = 10

batch_size = 10_000


class TestPostgisInfluxdb(TestCase):
    def test_it(self):
        loc_service = LocationService(GeopyLocationAPI())
        database_url = (
            f"postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
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


def measure_generator(sensors: list[Sensor]):
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

    await temperature_repo.init(reset=True)
    await temperature_repo.save_batch(measure_generator(sensors), chunk_size=batch_size)

    # Test de recherche spatiale
    async with uow.transaction():
        nearby_sensors = await uow.sensors().find_in_radius(CENTER, RADIUS_KM)
    print(f"\nCapteurs trouvés dans un rayon de {RADIUS_KM}km: {len(nearby_sensors)}")
    assert len(nearby_sensors) > 0

    if nearby_sensors:
        now = datetime.now(UTC)
        stats = temperature_repo.search(
            MeasureQuery(
                sources=nearby_sensors,
                period=Period.from_duration(
                    now.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                    timedelta(days=1),
                ),
            )
        )

        measurements = []

        print("\nStatistiques de température par capteur:")
        for measures in stats:
            print(f"\nCapteur: {measures.sensor.uid} {len(measures.measures)}")
            measurements.extend(measures.iter_tagged())

        heatmap_service = HeatmapService()
        heatmap = heatmap_service.compute_heatmap(measurements, min_distance=0.0)
        cv2.imwrite("heatmap.png", heatmap)


async def populate_sensors(
    loc_service: LocationService, uow: UnitOfWork
) -> list[Sensor]:

    locations = [
        *[
            loc_service.random_in_radius(CENTER, RADIUS_KM)
            for _ in range(SENSOR_NUMBER)
        ],
        # *loc_service.generate_french_locations(SENSOR_NUMBER),
    ]
    # Création des capteurs
    sensors = [
        Sensor(
            uid=f"FR{idx:05d}",
            measure_type="temperature",
            location=location,
        )
        for idx, location in enumerate(locations)
    ]
    async with uow.transaction():
        await uow.sensors().save(sensors)
    return sensors
