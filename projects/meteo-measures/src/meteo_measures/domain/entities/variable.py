from dataclasses import dataclass


@dataclass
class Variable:
    name: str
    coords: list[str]
