from dataclasses import dataclass
from unittest import TestCase

from dependency_injector import containers, providers


@dataclass
class MyConfig:
    param: str


class MyService:
    def __init__(self, custom: str, config: MyConfig):
        self.custom = custom
        self.config = config


class MyContainer(containers.DeclarativeContainer):
    config = providers.Singleton(MyConfig, param='toto')
    service_factory = providers.Factory(MyService, config=config)


class TestDependencyInjector(TestCase):
    def setUp(self):
        self.container = MyContainer()

    def test_it(self):
        service = self.container.service_factory(custom='coucou')
        print(service)
        print(service.config)
        print(service.custom)
        self.assertEqual(type(service), MyService)
