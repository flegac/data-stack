from abc import ABC
from typing import Type

from sqlalchemy import inspect


class ModelMapping[Entity, DbModel](ABC):

    def __init__(
        self,
        entity: Type[Entity],
        model: Type[DbModel],
    ):
        self.entity = entity
        self.model = model

    @property
    def primary_key(self):
        return inspect(self.model).primary_key[0]

    def extract_dict(self, item):
        return {
            k: v
            for k, v in item.__dict__.items()
            if k in inspect(self.model).column_attrs
        }

    def model_to_entity(self, model: DbModel) -> Entity:
        return self.entity(
            **self.extract_dict(model),
        )

    def entity_to_model(self, item: Entity) -> DbModel:
        return self.model(
            **self.extract_dict(item),
        )
