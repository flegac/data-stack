import asyncio
from unittest import TestCase

from message_queue.memory_mq_backend import MemoryMQBackend
from message_queue.mq_backend_checker import mq_backend_checker


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
