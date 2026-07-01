"""
ATLAS Event System (Lightweight Event Bus)
"""

from collections import defaultdict
from typing import Callable, Any


class EventBus:
    """
    Simple in-memory event bus for decoupled communication.
    """

    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[Any], None]):
        """
        Subscribe to an event.
        """
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, data: Any = None):
        """
        Publish an event to all subscribers.
        """
        if event_name not in self._subscribers:
            return

        for handler in self._subscribers[event_name]:
            handler(data)


# Global event bus instance
event_bus = EventBus()