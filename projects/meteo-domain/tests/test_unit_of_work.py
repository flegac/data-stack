import asyncio
import inspect
from dataclasses import dataclass
from unittest import TestCase

from event_mock.event_bus import event_mock
from meteo_domain.core.unit_of_work import UnitOfWork, WriteQuery


@dataclass
class DomainA:
    uid: str


@dataclass
class DomainB:
    uid: str


class SaveQuery[Entity](WriteQuery):
    def __init__(self, item: Entity):
        self.item = item

    def write(self, uow: UnitOfWork):
        pass


class TestMemoryUnitOfWork(TestCase):
    def test_all(self):
        for func in list_async_methods(self):
            with self.subTest(func.__name__):
                asyncio.run(func())

    async def full_transaction(self):
        a = DomainA(uid="A")
        b = DomainB(uid="B")
        c = DomainB(uid="C")

        uow, bus = event_mock(UnitOfWork)
        uow, bus = event_mock()
        async with uow.transaction():
            await uow.save(a)
            await uow.save(b)
            await uow.delete(b)
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            [
                "transaction()",
                "create_session()",
                "save(DomainA(uid='A'))",
                "save(DomainB(uid='B'))",
                "delete(DomainB(uid='B'))",
                "commit()",
                "destroy_session()",
            ],
        )
        bus.events.clear()
        async with uow.transaction():
            await uow.save(c)
            await uow.delete(a)
            uow.cancel("testing")
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            [
                "transaction()",
                "create_session()",
                "save(DomainB(uid='C'))",
                "delete(DomainA(uid='A'))",
                "cancel(testing)",
                "rollback()",
                "destroy_session()",
            ],
        )

    async def cancel_transaction(self):
        uow, bus = event_mock(UnitOfWork)

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
