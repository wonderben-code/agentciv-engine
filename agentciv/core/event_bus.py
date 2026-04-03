"""Event bus — pub/sub for all engine events.

Subscribers can be sync or async. The chronicle, CLI output, and any
external integrations subscribe to events here.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable

from .types import Event, EventType

log = logging.getLogger(__name__)

Subscriber = Callable[[Event], Any]


class EventBus:
    """Central event bus for the engine."""

    def __init__(self) -> None:
        self._subscribers: dict[EventType | None, list[Subscriber]] = defaultdict(list)
        self._log: list[Event] = []

    def subscribe(self, event_type: EventType | None, handler: Subscriber) -> None:
        """Subscribe to a specific event type, or None for all events."""
        self._subscribers[event_type].append(handler)

    def emit(self, event: Event) -> None:
        """Emit an event to all relevant subscribers."""
        self._log.append(event)

        # Notify specific subscribers
        for handler in self._subscribers.get(event.type, []):
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    asyncio.ensure_future(result)
            except Exception as e:
                log.debug("Event handler error: %s", e)

        # Notify wildcard subscribers
        for handler in self._subscribers.get(None, []):
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    asyncio.ensure_future(result)
            except Exception as e:
                log.debug("Event handler error: %s", e)

    def get_log(self, since_tick: int = 0) -> list[Event]:
        """Get all events since a given tick."""
        return [e for e in self._log if e.tick >= since_tick]

    def clear_log(self) -> None:
        """Clear the event log."""
        self._log.clear()
