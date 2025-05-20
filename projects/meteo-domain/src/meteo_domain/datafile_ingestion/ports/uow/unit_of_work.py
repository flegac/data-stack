from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from meteo_domain.datafile_ingestion.ports.uow.geo_repository import (
    GeoRepository,
)
from meteo_domain.datafile_ingestion.ports.uow.repository import Repository
from meteo_domain.geo_sensor.entities.geo_sensor import GeoSensor


class CancelUnitOfWorkError(Exception):
    def __init__(self, reason: str = None):
        self.reason = reason


class UnitOfWork(ABC):
    @abstractmethod
    def datafiles(self) -> Repository[DataFile]: ...

    @abstractmethod
    def workspaces(self) -> Repository[Workspace]: ...

    @abstractmethod
    def sensors(self) -> GeoRepository[GeoSensor]: ...

    @asynccontextmanager
    async def transaction(self):
        await self.on_start()
        try:
            yield
            await self.commit()
        except CancelUnitOfWorkError:
            await self.rollback()
        except Exception:
            await self.rollback()
            raise
        finally:
            await self.on_stop()

    @abstractmethod
    async def on_start(self): ...

    @abstractmethod
    async def on_stop(self): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    def cancel(self, reason: str = None):
        raise CancelUnitOfWorkError(reason=reason)
