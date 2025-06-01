from dataclasses import dataclass

from reports.domain.report.events import ReportDeleted
from reports.domain.report.repository import ReportRepository
from reports.domain.shared.events import DomainEventAdder
from reports.domain.types import ReportId
from reports.services.common.application_error import ApplicationError, ErrorType
from reports.services.common.handlers import RequestHandler
from reports.services.common.markers import Command
from reports.services.ports.identity_provider import IdentityProvider


@dataclass(frozen=True)
class DeleteDeviceReport(Command[None]):
    report_id: ReportId


class DeleteDeviceReportHandler(RequestHandler[DeleteDeviceReport, None]):
    def __init__(
        self,
        report_repository: ReportRepository,
        identity_provider: IdentityProvider,
        event_adder: DomainEventAdder,
    ) -> None:
        self._report_repository = report_repository
        self._identity_provider = identity_provider
        self._event_adder = event_adder

    def handle(self, request: DeleteDeviceReport) -> None:
        current_user_id = self._identity_provider.current_user_id()
        report = self._report_repository.device_report_with_id(
            report_id=request.report_id
        )

        if not report:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Report with id {request.report_id} not found",
            )

        if report.creator_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.FORBIDDEN,
                message=f"User {current_user_id} is not the creator of the report",
            )

        self._event_adder.add(event=ReportDeleted(report_id=request.report_id))

        self._report_repository.delete(report)
