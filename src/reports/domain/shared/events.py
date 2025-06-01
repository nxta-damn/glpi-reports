from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from reports.domain.shared.markers import Notification
from reports.domain.types import EventId


@dataclass(frozen=True, kw_only=True)
class DomainEvent(Notification):
    event_date: datetime | None = field(default=None, init=False)
    event_id: EventId | None = field(default=None, init=False)

    @property
    def event_type(self) -> str:
        return type(self).__name__

    def set_event_id(self, event_id: EventId) -> None:
        if self.event_id:
            return

        object.__setattr__(self, "event_id", event_id)

    def set_event_date(self, event_date: datetime) -> None:
        if self.event_date:
            return

        object.__setattr__(self, "event_date", event_date)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, DomainEvent):
            return NotImplemented

        return self.__dict__ == value.__dict__

    def __hash__(self) -> int:
        return hash(self.event_id)

    def __str__(self) -> str:
        return f"{self.event_type}({self.__dict__})"

    def __repr__(self) -> str:
        return self.__str__()


class DomainEventAdder(ABC):
    @abstractmethod
    def add(self, event: DomainEvent) -> None: ...
