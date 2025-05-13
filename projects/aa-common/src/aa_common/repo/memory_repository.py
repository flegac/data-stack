import datetime
from collections import defaultdict
from typing import override, Any, AsyncGenerator, Type

from aa_common.repo.repository import Repository, UID
from aa_common.repo.unit_of_work import UnitOfWork


class EventBus:
    def __init__(self):
        self.events: list[tuple[datetime.datetime, str]] = []

    def push(self, event: str):
        self.events.append((datetime.datetime.now(datetime.UTC), event))

    def sorted_events(self):
        return [event for time, event in sorted(self.events)]

    def __repr__(self):
        return f"{self.sorted_events()}"


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
    def __init__(self, events: EventBus):
        self.events = events
        self.backups: dict[type, Backup] = defaultdict(Backup)

    def on_update(self, item):
        self.push(f"on_update: {item.uid}")
        self.backups[type(item)].on_update(item)

    def on_create(self, item):
        self.push(f"on_create: {item.uid}")
        self.backups[type(item)].on_create(item)

    def on_delete(self, item):
        self.push(f"on_delete: {item.uid}")
        self.backups[type(item)].on_delete(item)

    def push(self, event: str):
        self.events.push(event)


class MemRepository[Entity](Repository[Entity]):
    def __init__(self, ctype: Entity, session: MemSession = None):
        self.ctype = ctype
        self.session = session
        self.items: dict[UID, Entity] = {}

    @override
    async def create_or_update(self, item: Entity) -> UID:
        if item.uid in self.items:
            self.session.on_update(item)
        else:
            self.session.on_create(item)
        self.items[item.uid] = item
        return item.uid

    @override
    async def insert_batch(self, items: list[Entity]) -> list[Entity]:
        for item in items:
            await self.create_or_update(item)
        return items

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


class MemUnitOfWork(UnitOfWork[MemSession]):
    def __init__(self):
        self.repositories: dict[type, MemRepository] = {}
        self.session: MemSession | None = None
        self.events: EventBus = EventBus()

    def sorted_events(self):
        return self.events.sorted_events()

    def clear_events(self):
        self.events = EventBus()

    def push(self, event: str):
        self.events.push(event)

    async def create_session(self):
        self.push("create_session")
        self.session = MemSession(self.events)
        return self.session

    async def destroy_session(self, session: MemSession):
        self.push("destroy_session")

    @override
    def repository[Entity](self, ctype: Type[Entity]):
        if ctype not in self.repositories:
            self.repositories[ctype] = MemRepository(ctype, self.session)
        self.repositories[ctype].session = self.session
        return self.repositories[ctype]

    @override
    async def commit(self, session: MemSession):
        self.push("commit")

    @override
    async def rollback(self, session: MemSession):
        self.push("rollback")
        for ctype, backup in session.backups.items():
            repo: MemRepository = self.repository(ctype)
            for uid, item in backup.updated.items():
                self.push(f"rollback: updated={uid}")
                repo.items[uid] = item
            for uid in backup.created:
                self.push(f"rollback: created={uid}")
                del repo.items[uid]
