from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Type

from aa_common.repo.repository import Repository


class CancelUnitOfWorkError(Exception):
    def __init__(self, reason: str = None):
        self.reason = reason


class UnitOfWork[Session](ABC):
    @asynccontextmanager
    async def transaction(self):
        session = await self.create_session()
        try:
            yield session
            await self.commit(session)
        except CancelUnitOfWorkError:
            await self.rollback(session)
        except Exception:
            await self.rollback(session)
            raise
        finally:
            await self.destroy_session(session)

    @abstractmethod
    async def create_session(self) -> Session: ...

    @abstractmethod
    async def destroy_session(self, session: Session): ...

    @abstractmethod
    async def commit(self, session: Session): ...

    @abstractmethod
    async def rollback(self, session: Session): ...

    def cancel(self, reason: str = None):
        raise CancelUnitOfWorkError(reason=reason)

    @abstractmethod
    def repository[Entity](self, entity: Type[Entity]) -> Repository[Entity]: ...

    async def save[Entity](self, item: Entity):
        await self.repository(type(item)).create_or_update(item)

    async def delete[Entity](self, item: Entity):
        await self.repository(type(item)).delete_by_id(item.uid)
