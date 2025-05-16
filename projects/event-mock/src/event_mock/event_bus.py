import datetime


class EventBus:
    def __init__(self):
        self.events: list[tuple[datetime.datetime, str]] = []

    def push(self, event: str):
        self.events.append((datetime.datetime.now(datetime.UTC), event))

    def sorted_events(self):
        return [event for time, event in sorted(self.events, key=lambda x: x[0])]

    def __repr__(self):
        return f"{self.sorted_events()}"
