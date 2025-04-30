from dataclasses import dataclass
from unittest import TestCase

from injector import Module, Binder, SingletonScope, Injector, Inject, ClassAssistedBuilder


@dataclass
class MyConfig:
    param: str


class MyService:
    def __init__(self, custom: str, config: Inject[MyConfig]):
        self.custom = custom
        self.config = config


class TestModule(Module):
    def configure(self, binder: Binder):
        binder.bind(MyConfig, to=MyConfig(param='toto'), scope=SingletonScope)


class TestInjector(TestCase):
    def setUp(self):
        self.__injector = Injector(TestModule)

    def test_it(self):
        builder = self.__injector.get(ClassAssistedBuilder[MyService])
        service = builder.build(custom='coucou')
        print(service)
        print(service.config)
        print(service.custom)
        self.assertEqual(type(service), MyService)
