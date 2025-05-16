from datetime import UTC, datetime, timedelta
from unittest import TestCase

from tqdm import tqdm

from influxdb_connector.influxdb_config import InfluxDBConfig
from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from meteo_domain.sensor.entities.location import Location
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.sensor.ports.sensor_repository import SensorRepository
from meteo_domain.temporal_series.entities.measure_query import MeasureQuery
from meteo_domain.temporal_series.entities.measurement import (
    TaggedMeasurement,
)
from meteo_domain.temporal_series.entities.period import Period
from meteo_domain.temporal_series.ports.tseries_repository import TSeriesRepository
from meteo_domain.utils import generate_french_locations
from sql_connector.sql_unit_of_work import SqlUnitOfWork
from sql_meteo_adapters.repositories import SqlSensorRepository

PARIS = Location(latitude=48.8566, longitude=2.3522)
search_radius_km = 500
locations = 100
period_hours = 200
batch_size = 1_000


async def weather_workflow(
    uow: SqlUnitOfWork,
    sensor_repo: SensorRepository,
    temperature_repo: TSeriesRepository,
):
    await temperature_repo.init(reset=True)

    # Création des capteurs
    sensors = [
        Sensor(
            uid=f"FR{idx:05d}",
            measure_type="temperature",
            location=location,
        )
        for idx, location in enumerate(generate_french_locations(locations))
    ]

    async with uow.transaction():
        await sensor_repo.save(sensors)

    # Ajout des mesures
    base_date = datetime.now(UTC).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    def measure_generator():
        for sensor in tqdm(sensors, f"generate {period_hours} measures per sensor"):
            for hour in range(period_hours):
                yield TaggedMeasurement(
                    time=base_date + timedelta(hours=hour),
                    value=20 + (hour % 10),
                    sensor=sensor,
                )

    await temperature_repo.save_batch(measure_generator(), chunk_size=batch_size)

    # Test de recherche spatiale
    nearby_sensors = await sensor_repo.find_in_radius(PARIS, search_radius_km)
    print(
        f"\nCapteurs trouvés dans un rayon de "
        f"{search_radius_km}km: {len(nearby_sensors)}"
    )

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
            # for record in table.records:
            #     print(record)
            #     print(
            #         f"Heure: {record.get_time()}, Moyenne: {record.get_value():.1f}°C"
            #     )


class TestPostgisInfluxdb(TestCase):
    def test_it(self):
        import asyncio

        uow = SqlUnitOfWork(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
        sensor_repo = SqlSensorRepository(uow)

        measures = InfluxDbMeasureRepository(
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
            )
        )
