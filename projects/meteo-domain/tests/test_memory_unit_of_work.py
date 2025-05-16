import asyncio
import inspect
from dataclasses import dataclass
from unittest import TestCase

from event_mock.event_bus import EventBus
from meteo_domain.core.unit_of_work import UnitOfWork


@dataclass
class DomainA:
    uid: str


@dataclass
class DomainB:
    uid: str


class TestMemoryUnitOfWork(TestCase):
    def test_all(self):
        for func in list_async_methods(self):
            with self.subTest(func.__name__):
                asyncio.run(func())

    async def cancel_transaction(self):
        bus = EventBus()
        uow = bus.mock_type(UnitOfWork)

        async with uow.transaction():
            uow.cancel("testing")

        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            [
                "transaction()",
                "create_session()",
                "cancel(testing)",
                "rollback()",
                "destroy_session()",
            ],
        )


def list_async_methods(obj):
    for name, method in inspect.getmembers(obj, inspect.iscoroutinefunction):
        yield method
