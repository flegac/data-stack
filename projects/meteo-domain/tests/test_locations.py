from unittest import TestCase

import numpy as np

from meteo_domain.geo_sensor.entities.location.locations import Locations


class TestLocations(TestCase):
    def test_locations(self):
        raw = np.random.rand(5, 2)
        batch = Locations.from_raw(raw)

        for loc in batch.iter():
            print(loc)


