import inspect
from unittest.mock import Mock

from event_mock.event_bus import EventBus


def method_tracer_async(bus: EventBus, object, func, is_abstract: bool = False):

    async def wrapper(*args, **kwargs):
        kwargs_str = "" if not kwargs else f"{kwargs}"
        args_str = "" if not args else f"{",".join(map(str,args))}"
        bus.push(f"{func.__name__}({args_str}{kwargs_str})")
        if not is_abstract:
            return await func(object, *args, **kwargs)
        return None

    return wrapper


def method_tracer(bus: EventBus, object, func, is_abstract: bool = False):

    def wrapper(*args, **kwargs):
        kwargs_str = "" if not kwargs else f"{kwargs}"
        args_str = "" if not args else f"{",".join(map(str,args))}"
        bus.push(f"{func.__name__}({args_str}{kwargs_str})")
        if not is_abstract:
            return func(object, *args, **kwargs)
        return None

    return wrapper


def event_mock[T](xxx: type[T], bus: EventBus | None = None) -> tuple[T, EventBus]:
    if bus is None:
        bus = EventBus()

    try:
        res = xxx()
    except:
        res = Mock()

    abstract_methods = xxx.__abstractmethods__
    # print(abstract_methods)

    for name, func in inspect.getmembers(xxx, inspect.isfunction):
        if name.startswith("_"):
            continue
        is_abstract = name in abstract_methods
        is_async = inspect.iscoroutinefunction(func)
        if is_async:
            method = method_tracer_async(bus, res, func, is_abstract)
        else:
            method = method_tracer(bus, res, func, is_abstract)
        # print(f"{name:20s}: is_abstract={is_abstract:1} is_async={is_async:1}")
        res.__setattr__(name, method)

    return res, bus
