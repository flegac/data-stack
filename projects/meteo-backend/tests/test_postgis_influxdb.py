from datetime import UTC, datetime, timedelta
from unittest import TestCase

from tqdm import tqdm
import asyncio

from geopy_location_api.geopy_location_compute_api import GeopyLocationAPI
from influxdb_connector.influxdb_config import InfluxDBConfig
from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbTSeriesRepository,
)
from meteo_domain.ports.sensor_repository import SensorRepository
from meteo_domain.ports.tseries_repository import TSeriesRepository
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.sensor.location_service import LocationService
from meteo_domain.temporal_series.entities.measure_query import MeasureQuery
from meteo_domain.temporal_series.entities.measurement import (
    TaggedMeasurement,
)
from meteo_domain.temporal_series.entities.period import Period
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.sensor import SqlSensorRepository

CENTER = Location(name="Paris", latitude=48.8566, longitude=2.3522)
RADIUS_KM = 50

SENSOR_NUMBER = 10
MEASUREMENT_PER_SENSOR = 10

batch_size = 10_000


async def weather_workflow(
    uow: SqlUnitOfWork,
    sensor_repo: SensorRepository,
    temperature_repo: TSeriesRepository,
    loc_service: LocationService,
):
    await uow.connection.kill_all_connections()
    await sensor_repo.drop_table()
    await sensor_repo.create_table()
    await temperature_repo.init(reset=True)

    locations = [
        *[loc_service.random_in_radius(CENTER, RADIUS_KM) for _ in range(10)],
        *loc_service.generate_french_locations(SENSOR_NUMBER),
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
        await sensor_repo.save(sensors)

    # Test de recherche spatiale
    nearby_sensors = await sensor_repo.find_in_radius(CENTER, RADIUS_KM)
    print(
        f"\nCapteurs trouvés dans un rayon de " f"{RADIUS_KM}km: {len(nearby_sensors)}"
    )
    assert len(nearby_sensors) > 0

    # Ajout des mesures
    base_date = datetime.now(UTC).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    def measure_generator():
        for sensor in tqdm(
            sensors, f"generate {MEASUREMENT_PER_SENSOR} measures per sensor"
        ):
            for hour in range(MEASUREMENT_PER_SENSOR):
                yield TaggedMeasurement(
                    time=base_date + timedelta(hours=hour),
                    value=20 + (hour % 10),
                    sensor=sensor,
                )

    await temperature_repo.save_batch(measure_generator(), chunk_size=batch_size)

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

        print("\nStatistiques de température par capteur:")
        for measures in stats:
            print(f"\nCapteur: {measures.sensor.uid} {len(measures.measures)}")
            # for measure in measures:
            #     print(measure)


class TestPostgisInfluxdb(TestCase):
    def test_it(self):

        loc_service = LocationService(GeopyLocationAPI())

        uow = SqlUnitOfWork(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
        sensor_repo = SqlSensorRepository(uow)

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
                sensor_repo,
                measures,
                loc_service,
            )
        )
