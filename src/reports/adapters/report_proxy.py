from datetime import datetime

from reports.adapters.persistence.sql_unit_of_work import UnitOfWork
from reports.domain.report.report import DeviceReport
from reports.domain.types import DeviceId, DeviceType, ReportId, UserId


class DeviceReportProxy:
    def __init__(
        self,
        device_report: DeviceReport,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._device_report = device_report
        self._unit_of_work = unit_of_work

    def edit(self, comment: str, report_name: str) -> None:
        self.change_comment(comment=comment)
        self.change_report_name(report_name=report_name)

    def change_comment(self, comment: str) -> None:
        if self._device_report.comment == comment:
            return

        self._device_report.change_comment(comment)
        self._unit_of_work.register_dirty(self._device_report)

    def change_report_name(self, report_name: str) -> None:
        if self._device_report.report_name == report_name:
            return

        self._device_report.change_report_name(report_name)
        self._unit_of_work.register_dirty(self._device_report)

    @property
    def entity_id(self) -> ReportId:
        return self._device_report.entity_id

    @property
    def creator_id(self) -> UserId:
        return self._device_report.creator_id

    @property
    def created_at(self) -> datetime:
        return self._device_report.created_at

    @property
    def comment(self) -> str:
        return self._device_report.comment

    @property
    def report_name(self) -> str:
        return self._device_report.report_name

    @property
    def device_id(self) -> DeviceId:
        return self._device_report.device_id

    @property
    def device_type(self) -> DeviceType:
        return self._device_report.device_type

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DeviceReportProxy):
            return NotImplemented

        return bool(other.entity_id == self.entity_id)

    def __hash__(self) -> int:
        return hash(self.entity_id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.entity_id})"

    def __repr__(self) -> str:
        return str(self)
