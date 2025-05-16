from collections import defaultdict
from collections.abc import AsyncGenerator
from typing import Any, override

from meteo_domain.core.repository import UID, Repository


class Backup[Entity]:
    def __init__(self):
        self.created: list[str] = []
        self.updated: dict[str, Entity] = {}

    def on_create(self, item: Entity):
        if self.is_known(item):
            return
        self.created.append(item.uid)

    def on_update(self, item: Entity):
        if self.is_known(item):
            return
        self.updated[item.uid] = item

    def on_delete(self, item: Entity):
        self.on_update(item)

    def is_known(self, item: Entity):
        return item.uid in self.created or item.uid in self.updated


class MemSession:
    def __init__(self):
        self.backups: dict[type, Backup] = defaultdict(Backup)

    def on_update(self, item):
        self.backups[type(item)].on_update(item)

    def on_create(self, item):
        self.backups[type(item)].on_create(item)

    def on_delete(self, item):
        self.backups[type(item)].on_delete(item)

    def __repr__(self):
        return f"MemSession"


class MemRepository[Entity](Repository[Entity]):
    def __init__(self, ctype: Entity, session: MemSession = None):
        self.ctype = ctype
        self.session = session
        self.items: dict[UID, Entity] = {}

    @override
    async def save(self, batch: Entity | list[Entity]):
        items = [batch]
        if isinstance(batch, list):
            items = batch
        for item in items:
            if item.uid in self.items:
                self.session.on_update(item)
            else:
                self.session.on_create(item)
            self.items[item.uid] = item

    @override
    async def delete_by_id(self, primary_key: UID):
        self.session.on_delete(self.items[primary_key])
        self.items.pop(primary_key)

    @override
    async def find_by_id(self, primary_key: UID) -> Entity | None:
        return self.items.get(primary_key)

    @override
    def find_all(self, **query: Any) -> AsyncGenerator[Entity, Any]:
        for item in self.items.values():
            yield item

    @override
    async def init(self, reset: bool = False):
        pass
