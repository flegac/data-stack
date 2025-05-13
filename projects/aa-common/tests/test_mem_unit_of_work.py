import asyncio
import inspect
from dataclasses import dataclass
from unittest import TestCase

from aa_common.repo.memory_repository import MemUnitOfWork


@dataclass
class DomainA:
    uid: str


@dataclass
class DomainB:
    uid: str


class TestMemoryMQBackend(TestCase):
    def test_all(self):
        for func in list_async_methods(self):
            with self.subTest(func.__name__):
                asyncio.run(func())

    async def full_transaction(self):
        a = DomainA(uid="A")
        b = DomainB(uid="B")
        c = DomainB(uid="C")
        d = DomainB(uid="D")
        e = DomainA(uid="E")

        uow = MemUnitOfWork()
        async with uow.transaction():
            await uow.save(a)
            await uow.save(b)
            await uow.delete(b)
        print(uow.events)
        self.assertListEqual(
            uow.sorted_events(),
            [
                "create_session",
                "on_create: A",
                "on_create: B",
                "on_delete: B",
                "commit",
                "destroy_session",
            ],
        )
        uow.clear_events()
        async with uow.transaction():
            await uow.save(c)
            await uow.delete(a)
            uow.cancel("testing")
        print(uow.events)
        self.assertListEqual(
            uow.sorted_events(),
            [
                "create_session",
                "on_create: C",
                "on_delete: A",
                "rollback",
                "rollback: created=C",
                "rollback: updated=A",
                "destroy_session",
            ],
        )

    async def cancel_transaction(self):
        uow = MemUnitOfWork()

        async with uow.transaction():
            uow.cancel("testing")

        print(uow.events)
        self.assertListEqual(
            uow.events.sorted_events(),
            ["create_session", "rollback", "destroy_session"],
        )


def list_async_methods(obj):
    for name, method in inspect.getmembers(obj, inspect.iscoroutinefunction):
        yield method
