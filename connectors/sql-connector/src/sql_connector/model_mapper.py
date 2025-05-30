from dataclasses import fields
from functools import cached_property

from sqlalchemy import inspect, Column
from sqlalchemy.orm import class_mapper

from sql_connector.patches.patch import MapperPatch
from sql_connector.sql_connection import BaseModel


class ModelMapper[Domain, Model: type[BaseModel]]:
    def __init__(
        self,
        domain: type[Domain],
        model: type[Model],
        patches: list[MapperPatch] = None,
    ):
        self.domain = domain
        self.model = model
        self.patches = patches or []

    def to_domain(self, model: Model) -> Domain:
        data = self.extract_dict(model)
        for patch in self.patches:
            data = patch.model.apply(data)
        return self.domain(**data)

    def to_model(self, domain: Domain) -> Model:
        data = self.extract_dict(domain)
        for patch in self.patches:
            data = patch.domain.apply(data)
        return self.model(**data)

    def extract_dict(self, data: Domain | Model) -> dict:
        return {key: getattr(data, key) for key in self.domain_attrs & self.model_attrs}

    @cached_property
    def primary_key(self) -> str:
        return self.primary_key_column.name

    @cached_property
    def primary_key_column(self) -> Column:
        return get_primary_key_column(self.model)

    @cached_property
    def domain_attrs(self):
        return {_.name for _ in fields(self.domain)}

    @cached_property
    def model_attrs(self):
        mapper = class_mapper(self.model)
        return {column.key for column in mapper.columns}


def get_primary_key_column(model) -> Column:
    inspector = inspect(model)
    if not (primary_key := inspector.primary_key):
        raise ValueError("Le modèle n'a pas de primary key définie.")
    return primary_key[0]
