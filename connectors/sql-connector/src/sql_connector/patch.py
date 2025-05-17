from abc import ABC, abstractmethod
from typing import Any


class Patch(ABC):
    @abstractmethod
    def select(self, name: str, value: Any) -> bool: ...

    @abstractmethod
    def patch(self, name: str, value: Any) -> tuple[str, Any]: ...

    def apply(self, item: dict[str, Any]) -> dict[str, Any]:
        res = {}
        for name, value in item.items():
            if self.select(name, value):
                new_name, new_value = self.patch(name, value)
                res[new_name] = new_value
            else:
                res[name] = value
        return res


class MapperPatch:
    def __init__(self, domain: Patch, model: Patch):
        self.domain = domain
        self.model = model
