from typing import cast

from reports.adapters.persistence.sql_unit_of_work import UnitOfWork
from reports.adapters.report_proxy import DeviceReportProxy
from reports.domain.report.events import DeviceReportCreated
from reports.domain.report.factory import ReportFactory
from reports.domain.report.report import DeviceReport
from reports.domain.shared.events import DomainEventAdder
from reports.domain.types import DeviceId, DeviceType, UserId
from reports.services.ports.id_generator import IdGenerator
from reports.services.ports.time_provider import TimeProvider


class ReportFactoryImlp(ReportFactory):
    def __init__(
        self,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._id_generator = id_generator
        self._time_provider = time_provider
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work

    def create_device_report(
        self,
        report_name: str,
        comment: str,
        device_id: DeviceId,
        device_type: DeviceType,
        creator_id: UserId,
    ) -> DeviceReport:
        device_report = DeviceReport(
            report_name=report_name,
            event_adder=self._event_adder,
            entity_id=self._id_generator.report_id(),
            creator_id=creator_id,
            comment=comment,
            created_at=self._time_provider.current(),
            device_id=device_id,
            device_type=device_type,
        )

        self._event_adder.add(
            event=DeviceReportCreated(
                report_id=device_report.entity_id,
                report_name=device_report.report_name,
                comment=device_report.comment,
                creator_id=device_report.creator_id,
                device_id=device_report.device_id,
                device_type=device_report.device_type,
            )
        )

        return cast("DeviceReport", DeviceReportProxy(device_report, self._unit_of_work))
