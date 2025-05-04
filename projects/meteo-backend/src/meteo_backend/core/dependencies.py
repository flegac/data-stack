from functools import lru_cache

from meteo_backend.core.application_context import ApplicationContext


@lru_cache
def get_context() -> ApplicationContext:
    from meteo_backend.core.config.container import Container

    return ApplicationContext.from_container(Container)
