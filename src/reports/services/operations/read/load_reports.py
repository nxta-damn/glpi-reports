from dataclasses import dataclass

from reports.services.common.handlers import RequestHandler
from reports.services.common.markers import Query
from reports.services.models.pagination import Pagination
from reports.services.models.report import ReportReadModel
from reports.services.ports.identity_provider import IdentityProvider
from reports.services.ports.report_gateway import ReportGateway


@dataclass(frozen=True)
class LoadReports(Query[list[ReportReadModel]]):
    pagination: Pagination


class LoadReportsHandler(RequestHandler[LoadReports, list[ReportReadModel]]):
    def __init__(
        self, identity_provider: IdentityProvider, report_gateway: ReportGateway
    ) -> None:
        self._identity_provider = identity_provider
        self._report_gateway = report_gateway

    def handle(self, request: LoadReports) -> list[ReportReadModel]:
        self._identity_provider.current_user_id()

        reports = self._report_gateway.load_many(pagination=request.pagination)

        return reports
