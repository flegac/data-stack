from meteo_domain.entities.geo_spatial.location import Location


def generate_french_locations(n: int):
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
