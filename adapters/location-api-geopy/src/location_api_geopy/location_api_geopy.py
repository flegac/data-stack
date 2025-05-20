import random
from typing import override

from geopy import Point
from geopy.distance import geodesic
from meteo_domain.datafile_ingestion.ports.location_api import LocationAPI
from meteo_domain.geo_sensor.entities.location.location import Location


class GeopyLocationAPI(LocationAPI):
    @override
    def haversine_distance(self, loc1: Location, loc2: Location) -> float:
        """Calcule la distance entre deux locations en utilisant geopy."""
        point1 = Point(loc1.latitude, loc1.longitude)
        point2 = Point(loc2.latitude, loc2.longitude)
        return geodesic(point1, point2).km

    @override
    def random_in_radius(self, center: Location, radius_km: float) -> Location:
        """Génère des points aléatoires à la surface de la Terre dans un rayon donné."""
        # Générer un angle et une distance aléatoires
        angle = random.uniform(0, 360)
        distance = random.uniform(0, radius_km)

        # Calculer les nouvelles coordonnées
        destination = geodesic(kilometers=distance).destination(
            Point(center.latitude, center.longitude), angle
        )

        # Ajouter la nouvelle localisation à la liste
        location = Location(
            latitude=destination.latitude, longitude=destination.longitude
        )
        dist = self.haversine_distance(center, location)
        assert dist <= radius_km, (
            "Location outside radius: {dist:.1f}km > {radius_km:.1f}km"
        )

        return location
