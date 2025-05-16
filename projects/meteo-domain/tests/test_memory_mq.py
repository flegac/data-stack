import asyncio
from unittest import TestCase

from meteo_domain.core.impl.memory_mq_backend import MemoryMQBackend
from meteo_domain.core.impl.mq_backend_checker import mq_backend_checker


class TestMemoryMQBackend(TestCase):
    def test_it(self):
        backend = MemoryMQBackend()
        asyncio.run(
            mq_backend_checker(
                backend,
                message_number=3,
                timeout_sec=0.25,
            )
        )
