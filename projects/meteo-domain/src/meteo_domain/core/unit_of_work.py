from abc import ABC, abstractmethod
from contextlib import asynccontextmanager


class CancelUnitOfWorkError(Exception):
    def __init__(self, reason: str = None):
        self.reason = reason


class UnitOfWork(ABC):
    @asynccontextmanager
    async def transaction(self):
        await self.create_session()
        try:
            yield
            await self.commit()
        except CancelUnitOfWorkError:
            await self.rollback()
        except Exception:
            await self.rollback()
            raise
        finally:
            await self.destroy_session()

    @abstractmethod
    async def create_session(self): ...

    @abstractmethod
    async def destroy_session(self): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    def cancel(self, reason: str = None):
        raise CancelUnitOfWorkError(reason=reason)
