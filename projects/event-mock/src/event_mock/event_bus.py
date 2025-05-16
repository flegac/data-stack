import datetime
import inspect
from unittest.mock import Mock


class EventBus:
    def __init__(self):
        self.events: list[tuple[datetime.datetime, str]] = []

    def push(self, event: str):
        self.events.append((datetime.datetime.now(datetime.UTC), event))

    def sorted_events(self):
        return [event for time, event in sorted(self.events, key=lambda x: x[0])]

    def __repr__(self):
        return f"{self.sorted_events()}"

    def mock_object[T](self, obj: T) -> T:
        for name, func in inspect.getmembers(obj, inspect.isroutine):
            if name.startswith("_"):
                continue
            method = self._wrap_object_func(obj, func)
            obj.__setattr__(name, method)

        return obj

    def mock_type[T](self, klass: type[T]) -> T:
        res = Mock()

        abstract_methods = klass.__abstractmethods__
        for name, func in inspect.getmembers(klass, inspect.isfunction):
            if name.startswith("_"):
                continue
            is_abstract = name in abstract_methods
            method = self._wrap_type_func(res, func, is_abstract)
            res.__setattr__(name, method)

        return res

    def _trace_func(self, func, *args, **kwargs):
        kwargs_str = "" if not kwargs else f"{kwargs}"
        args_str = "" if not args else f"{','.join(map(str, args))}"
        self.push(f"{func.__name__}({args_str}{kwargs_str})")

    def _wrap_object_func(self, object, func):
        is_async = inspect.iscoroutinefunction(func)
        print(f"{func.__name__:20s}: is_async={is_async:1}")

        if is_async:

            async def wrapper(*args, **kwargs):
                self._trace_func(func, *args, **kwargs)
                return await func(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                self._trace_func(func, *args, **kwargs)
                return func(*args, **kwargs)

        return wrapper

    def _wrap_type_func(self, object, func, is_abstract: bool):
        is_async = inspect.iscoroutinefunction(func)
        print(f"{func.__name__:20s}: is_abstract={is_abstract:1} is_async={is_async:1}")

        if is_async:

            async def wrapper(*args, **kwargs):
                self._trace_func(func, *args, **kwargs)
                if is_abstract:
                    return None
                return await func(object, *args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                self._trace_func(func, *args, **kwargs)
                if is_abstract:
                    return None
                return func(object, *args, **kwargs)

        return wrapper
