import asyncio
from unittest import TestCase

from aa_common.mq.memory_mq_backend import MemoryMQBackend
from aa_common.mq.mq_backend_checker import mq_backend_checker


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
