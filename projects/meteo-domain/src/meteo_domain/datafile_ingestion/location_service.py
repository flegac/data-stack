from meteo_domain.datafile_ingestion.ports.location_api import LocationAPI
from meteo_domain.measurement.entities.sensor.location import Location


class LocationService:
    def __init__(self, location_api: LocationAPI):
        self.location_api = location_api

    def random_in_radius(self, center: Location, radius_km: float) -> Location:
        return self.location_api.random_in_radius(center, radius_km)

    def generate_french_locations(self, n: int) -> list[Location]:
        """Génère n positions aléatoires en France métropolitaine"""
        import random

        # Limites approximatives de la France métropolitaine
        min_lat, max_lat = (41.0, 51.5)  # Corse du Sud, Dunkerque
        min_lon, max_lon = (-5.0, 9.0)  # Bretagne, Alsace

        return [
            Location(
                latitude=random.uniform(min_lat, max_lat),
                longitude=random.uniform(min_lon, max_lon),
            )
            for _ in range(n)
        ]
