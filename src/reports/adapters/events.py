from collections.abc import Iterable

from reports.domain.shared.events import DomainEvent, DomainEventAdder
from reports.services.ports.events import DomainEventsRaiser


class DomainEvents(DomainEventsRaiser, DomainEventAdder):
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def add(self, event: DomainEvent) -> None:
        self._events.append(event)

    def raise_events(self) -> Iterable[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
