import asyncio
from datetime import datetime, UTC, timedelta

from tqdm import tqdm

from influxdb_connector.influxdb_config import InfluxDBConfig
from influxdb_measure_repository.influxdb_measure_repository import (
    InfluxDbMeasureRepository,
)
from meteo_domain.entities.geo_spatial.location import Location
from meteo_domain.entities.measure_query import MeasureQuery
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.entities.sensor import Sensor
from meteo_domain.entities.temporal.period import Period
from meteo_domain.utils import generate_french_locations
from sql_connector.sql_connection import SqlConnection
from sql_meteo_adapters.sensor_repository import SqlSensorRepository


async def test_weather_db():
    PARIS = Location(latitude=48.8566, longitude=2.3522)
    search_radius_km = 500
    locations = 100
    period_hours = 200
    batch_size = 200_000

    # repositories
    sensor_repo = SqlSensorRepository(
        SqlConnection(
            "postgresql+asyncpg://admin:adminpassword@localhost:5432/meteo-db"
        )
    )
    temperature_repo = InfluxDbMeasureRepository(
        InfluxDBConfig(
            url="http://localhost:8086",
            token="server-token",
            org="myorg",
            bucket="meteo-data",
        )
    )

    await sensor_repo.init(reset=True)
    await temperature_repo.init()

    # Création des capteurs
    sensors = [
        Sensor(
            uid=f"FR{idx:05d}",
            measure_type="temperature",
            location=location,
        )
        for idx, location in enumerate(generate_french_locations(locations))
    ]
    await sensor_repo.insert_batch(sensors)

    # Ajout des mesures
    base_date = datetime.now(UTC).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    def measure_generator():
        for sensor in tqdm(sensors, f"generate {period_hours} measures per sensor"):
            for hour in range(period_hours):
                yield Measurement(
                    sensor=sensor,
                    time=base_date + timedelta(hours=hour),
                    value=20 + (hour % 10),
                )

    await temperature_repo.save_batch(measure_generator(), chunk_size=batch_size)

    # Test de recherche spatiale
    nearby_sensors = await sensor_repo.find_in_radius(PARIS, search_radius_km)
    print(
        f"\nCapteurs trouvés dans un rayon de {search_radius_km}km: {len(nearby_sensors)}"
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
            print(f"\nCapteur: {measures.sensor.uid} { len(measures.measures)}")
            # for record in table.records:
            #     print(record)
            #     print(
            #         f"Heure: {record.get_time()}, Moyenne: {record.get_value():.1f}°C"
            #     )


if __name__ == "__main__":
    asyncio.run(test_weather_db())
