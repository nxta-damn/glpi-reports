from abc import ABC, abstractmethod

from reports.domain.types import ReportId
from reports.services.models.pagination import Pagination
from reports.services.models.report import ReportReadModel


class ReportGateway(ABC):
    @abstractmethod
    def load_many(self, pagination: Pagination) -> list[ReportReadModel]: ...
    @abstractmethod
    def with_id(self, report_id: ReportId) -> ReportReadModel | None: ...
