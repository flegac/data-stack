import asyncio
from abc import abstractmethod, ABC
from unittest import TestCase

from event_mock.event_mock import event_mock


class MyClass(ABC):

    @abstractmethod
    def abstract(self): ...
    @abstractmethod
    async def abstract_async(self): ...

    def not_abstract(self):
        return self.sub_method("not_abstract")

    async def not_abstract_async(self):
        return self.sub_method("not_abstract_async")

    def sub_method(self, param: str):
        return "sub_method"


class TestIt(TestCase):

    def test_it(self):
        asyncio.run(self.check_it())

    async def check_it(self):
        mock, bus = event_mock(MyClass)

        mock.abstract()
        await mock.abstract_async()

        mock.not_abstract()
        await mock.not_abstract_async()

        print(bus)
        self.assertListEqual(
            bus.sorted_events(),
            [
                "abstract()",
                "abstract_async()",
                "not_abstract()",
                "sub_method(not_abstract)",
                "not_abstract_async()",
                "sub_method(not_abstract_async)",
            ],
        )
