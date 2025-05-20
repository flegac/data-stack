import datetime
from unittest import TestCase

import numpy as np

from meteo_domain.core.logger import logger
from meteo_domain.geo_sensor.entities.times.period import Period
from meteo_domain.geo_sensor.entities.times.times import Times


class TestTimes(TestCase):
    def test_check_dtype(self):
        with self.assertRaises(AssertionError):
          Times.from_raw(np.array([1, 2, 3]))

    def test_times(self):
        batch = Period.from_duration(datetime.datetime.now(), datetime.timedelta(days=1)).split(5)
        self.assertIsInstance(batch, Times)

        for loc in batch:
            logger.info(loc)
