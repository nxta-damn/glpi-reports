from uuid_extensions import uuid7

from reports.domain.types import EventId, ReportId
from reports.services.ports.id_generator import IdGenerator


class UUID7IdGenerator(IdGenerator):
    def report_id(self) -> ReportId:
        return ReportId(uuid7())

    def event_id(self) -> EventId:
        return EventId(uuid7())
