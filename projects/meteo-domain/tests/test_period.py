import datetime
from unittest import TestCase

from meteo_domain.measurement.entities.period import Period


class TestPeriod(TestCase):
    def test_split(self):

        period = Period.from_duration(
            datetime.datetime.now(), datetime.timedelta(days=1)
        )

        times = period.split(23)

        self.assertEqual(len(times), 25)
        for time in times:
            self.assertEqual(time.minute, period.start.minute)
            self.assertEqual(time.second, period.start.second)
            self.assertEqual(time.microsecond, period.start.microsecond)
