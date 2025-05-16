from unittest import TestCase

from event_mock.event_bus import EventBus


class TestEventBus(TestCase):
    def test_push(self):
        self.event_bus = EventBus()
        self.event_bus.push("Event 1")
        self.event_bus.push("Event 2")
        self.assertEqual(self.event_bus.sorted_events(), ["Event 1", "Event 2"])
