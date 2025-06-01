from abc import ABC, abstractmethod

from reports.domain.types import EventId, ReportId


class IdGenerator(ABC):
    @abstractmethod
    def report_id(self) -> ReportId: ...
    @abstractmethod
    def event_id(self) -> EventId: ...
