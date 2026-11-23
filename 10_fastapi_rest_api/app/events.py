from collections import defaultdict
from typing import Any, Callable

Handler = Callable[[dict[str, Any]], None]


class EventBus:
    """Minimal in-process publish/subscribe bus.

    Producers publish events without knowing the consumers (decoupling), which is
    the core idea of event-driven architecture.
    """

    def __init__(self):
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self.history: list[tuple[str, dict]] = []

    def subscribe(self, event: str, handler: Handler) -> None:
        self._handlers[event].append(handler)

    def publish(self, event: str, payload: dict[str, Any]) -> None:
        self.history.append((event, payload))
        for handler in self._handlers[event]:
            handler(payload)
