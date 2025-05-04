from dataclasses import dataclass


@dataclass
class Variable:
    name: str
    coords: list[str]

    def __repr__(self):
        return f"{self.name}{self.coords}"
