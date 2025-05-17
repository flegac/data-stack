import asyncio
from abc import ABC, abstractmethod
from unittest import TestCase

from event_mock.event_bus import EventBus


class AbstractSync(ABC):
    @abstractmethod
    def func(self): ...


class AbstractAsync(ABC):
    @abstractmethod
    async def func(self): ...


class ConcreteSync:
    def func(self):
        self.sub_func("func")

    def sub_func(self, param: str):
        return f"sub_func: {self}"


class ConcreteAsync:
    async def func(self):
        await self.sub_func("func")

    async def sub_func(self, param: str):
        return f"sub_func: {self}"


class TestIt(TestCase):
    def test_concrete_sync(self):
        # Given
        bus = EventBus()
        mock = bus.mock_object(ConcreteSync())

        # When
        mock.func()

        # Then
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            ["func()", "sub_func(func)"],
        )

    def test_concrete_async(self):
        # Given
        bus = EventBus()
        mock = bus.mock_object(ConcreteAsync())

        # When
        asyncio.run(mock.func())

        # Then
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            ["func()", "sub_func(func)"],
        )

    def test_abstract_sync(self):
        # Given
        bus = EventBus()
        mock = bus.mock_type(AbstractSync)

        # When
        mock.func()

        # Then
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            ["func()"],
        )

    def test_abstract_async(self):
        # Given
        bus = EventBus()
        mock = bus.mock_type(AbstractAsync)

        # When
        asyncio.run(mock.func())

        # Then
        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            ["func()"],
        )
