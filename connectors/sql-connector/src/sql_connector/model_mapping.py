from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Protocol, override

from pydantic import BaseModel
from sqlmodel import SQLModel


class ModelDomainMapper[Domain, Model](ABC):
    @abstractmethod
    def to_model(self, domain: Domain) -> Model: ...

    @abstractmethod
    def to_domain(self, model: Model) -> Domain: ...

    @abstractmethod
    def primary_key(self) -> str: ...


class DictConvertible(Protocol):
    """Protocol pour les types convertibles en dict (dataclass ou BaseModel)"""

    def __dict__(self) -> dict[str, Any]: ...


class ModelMapping[
    Domain: DictConvertible | type[dataclass],
    Model: type[SQLModel],
](ModelDomainMapper[Domain, Model]):
    def __init__(
        self,
        domain: type[Domain],
        model: type[Model],
    ):
        self.entity = domain
        self.model = model

    @override
    def primary_key(self) -> str:
        return self.model.__table__.primary_key.columns.values()[0].name

    @override
    def to_domain(self, model: Model) -> Domain:
        return self.entity(**self._extract_dict(model))

    @override
    def to_model(self, entity: Domain) -> Model:
        data = self._extract_dict(entity)
        return self.model(**data)

    def _extract_dict(self, obj: Domain | Model) -> dict[str, Any]:
        return obj.model_dump() if isinstance(obj, BaseModel) else asdict(obj)
