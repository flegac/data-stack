from typing import override

from meteo_domain.core.impl.memory_repository import MemRepository, MemSession
from meteo_domain.core.unit_of_work import UnitOfWork


class MemUnitOfWork(UnitOfWork):

    def __init__(self):
        self.repositories: dict[type, MemRepository] = {}
        self.session: MemSession | None = None

    @override
    async def create_session(self):
        self.session = MemSession()

    @override
    async def destroy_session(self):
        pass

    def _repository[Entity](self, ctype: type[Entity]):
        if ctype not in self.repositories:
            self.repositories[ctype] = MemRepository(ctype, self.session)
        self.repositories[ctype].session = self.session
        return self.repositories[ctype]

    @override
    async def commit(self):
        pass

    @override
    async def rollback(self):
        for ctype, backup in self.session.backups.items():
            repo: MemRepository = self._repository(ctype)
            for uid, item in backup.updated.items():
                repo.items[uid] = item
            for uid in backup.created:
                del repo.items[uid]

    @override
    async def save[Entity](self, item: Entity | list[Entity]):
        await self._repository(type(item)).save(item)

    @override
    async def delete[Entity](self, item: Entity):
        await self._repository(type(item)).delete_by_id(item.uid)
