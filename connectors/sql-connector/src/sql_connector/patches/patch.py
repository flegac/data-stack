from abc import ABC, abstractmethod
from typing import Any


class Patch(ABC):
    @abstractmethod
    def select(self, name: str, value: Any) -> bool: ...

    @abstractmethod
    def patch(self, value: Any) -> Any: ...

    def apply(self, item: dict[str, Any]) -> dict[str, Any]:
        for name, value in item.items():
            if self.select(name, value):
                item[name] = self.patch(value)
        return item


class MapperPatch:
    def __init__(self, domain: Patch, model: Patch):
        self.domain = domain
        self.model = model
