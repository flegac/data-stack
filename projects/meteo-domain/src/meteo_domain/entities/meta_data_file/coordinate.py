from dataclasses import dataclass
from datetime import datetime
from typing import Generic, SupportsFloat, SupportsInt, TypeVar

T = TypeVar("T", bound=SupportsFloat | SupportsInt | datetime)


@dataclass
class Coordinate(Generic[T]):
    name: str
    values: list[T]

    @staticmethod
    def interval[Item](
        name: str,
        start: Item,
        end: Item,
        steps: int,
    ):
        total = end - start
        delta = total / (steps - 1) if steps > 1 else total
        values: list[Item] = [start + (delta * i) for i in range(steps)]
        return Coordinate(name, values)

    @property
    def size(self):
        return len(self.values)
