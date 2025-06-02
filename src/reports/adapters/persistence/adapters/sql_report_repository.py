from typing import cast

from sqlalchemy import Connection, Row, text

from reports.adapters.persistence.sql_unit_of_work import UnitOfWork
from reports.adapters.report_proxy import DeviceReportProxy
from reports.domain.report.report import DeviceReport
from reports.domain.report.repository import ReportRepository
from reports.domain.shared.events import DomainEventAdder
from reports.domain.types import ReportId


class SqlReportRepository(ReportRepository):
    def __init__(
        self,
        connection: Connection,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._connection = connection
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work
        self._identity_map: dict[ReportId, DeviceReport] = {}

    def add(self, report: DeviceReport) -> None:
        proxy = cast("DeviceReportProxy", report)
        self._unit_of_work.register_new(proxy._device_report)  # noqa: SLF001
        self._identity_map[proxy.entity_id] = proxy._device_report  # noqa: SLF001

    def delete(self, report: DeviceReport) -> None:
        proxy = cast("DeviceReportProxy", report)
        self._unit_of_work.register_deleted(proxy._device_report)  # noqa: SLF001
        self._identity_map.pop(proxy.entity_id, None)

    def with_device_id(self, device_id: ReportId) -> list[DeviceReport]:
        stmt = text(
            """
            SELECT * FROM device_reports WHERE device_id = :device_id
            """
        )
        result = self._connection.execute(stmt, {"device_id": device_id})
        rows = result.scalars().all()

        device_reports: list[DeviceReport] = []
        for row in rows:
            device_reports.append(report := self._load(row))
            self._identity_map[report.entity_id] = report

        return [
            cast("DeviceReport", DeviceReportProxy(report, self._unit_of_work))
            for report in device_reports
        ]

    def device_report_with_id(self, report_id: ReportId) -> DeviceReport | None:
        if report_id in self._identity_map:
            return cast(
                "DeviceReport",
                DeviceReportProxy(self._identity_map[report_id], self._unit_of_work),
            )

        stmt = text(
            """
            SELECT * FROM device_reports WHERE report_id = :report_id
            """
        )
        result = self._connection.execute(stmt, {"report_id": report_id})
        rows: Row | None = result.fetchone()

        if not rows:
            return None

        device_report = self._load(rows)
        self._identity_map[device_report.entity_id] = device_report
        return cast("DeviceReport", DeviceReportProxy(device_report, self._unit_of_work))

    def _load(self, row: Row) -> DeviceReport:
        report = DeviceReport(
            entity_id=row.report_id,
            event_adder=self._event_adder,
            creator_id=row.creator_id,
            comment=row.comment,
            created_at=row.created_at,
            report_name=row.report_name,
            device_id=row.device_id,
            device_type=row.device_type,
        )
        return report
