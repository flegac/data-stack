from abc import ABC, abstractmethod


class TimeRepository[Entity](ABC):
    @abstractmethod
    async def find_in_period(
        self,
        start: str,
        end: str,
    ) -> list[Entity]: ...
