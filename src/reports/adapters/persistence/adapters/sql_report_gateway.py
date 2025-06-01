from sqlalchemy import Connection, Row, text

from reports.domain.types import ReportId
from reports.services.models.pagination import Pagination
from reports.services.models.report import ReportReadModel
from reports.services.ports.report_gateway import ReportGateway


class SqlReportGateway(ReportGateway):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection
        self._identity_map: dict[ReportId, ReportReadModel] = {}

    def load_many(self, pagination: Pagination) -> list[ReportReadModel]:
        stmt = text(
            """
            SELECT * FROM device_reports LIMIT :limit OFFSET :offset
            """
        )
        result = self._connection.execute(
            stmt, {"limit": pagination.limit, "offset": pagination.offset}
        )
        rows = result.fetchall()

        device_reports: list[ReportReadModel] = []
        for row in rows:
            device_reports.append(report := self._load(row))
            self._identity_map[report.report_id] = report

        return device_reports

    def with_id(self, report_id: ReportId) -> ReportReadModel | None:
        stmt = text(
            """
            SELECT * FROM device_reports WHERE report_id = :report_id
            """
        )
        result = self._connection.execute(stmt, {"report_id": report_id})
        row: Row | None = result.fetchone()

        return self._load(row) if row else None

    def _load(self, row: Row) -> ReportReadModel:
        report = ReportReadModel(
            report_id=row.report_id,
            creator_id=row.creator_id,
            comment=row.comment,
            created_at=row.created_at,
            report_name=row.report_name,
            device_id=row.device_id,
            device_type=row.device_type,
        )
        return report
