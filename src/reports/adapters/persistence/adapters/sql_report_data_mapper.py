from sqlalchemy import Connection, text

from reports.adapters.persistence.sql_data_mapper import DataMapper
from reports.domain.report.report import DeviceReport


class SqlDeviceReportDataMapper(DataMapper[DeviceReport]):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def insert(self, model: DeviceReport) -> None:
        stmt = text(
            """
            INSERT INTO device_reports
            (report_id, creator_id, created_at, comment,
            report_name, device_id, device_type)
            VALUES
            (:report_id, :creator_id, :created_at, :comment,
            :report_name, :device_id, :device_type)
            """
        )

        self._connection.execute(
            stmt,
            {
                "report_id": model.entity_id,
                "creator_id": model.creator_id,
                "created_at": model.created_at,
                "comment": model.comment,
                "report_name": model.report_name,
                "device_id": model.device_id,
                "device_type": model.device_type,
            },
        )

    def update(self, model: DeviceReport) -> None:
        stmt = text(
            """
            UPDATE device_reports SET comment = :comment, report_name = :report_name
            WHERE report_id = :report_id
            """
        )

        self._connection.execute(
            stmt,
            {
                "comment": model.comment,
                "report_name": model.report_name,
                "report_id": model.entity_id,
            },
        )

    def delete(self, model: DeviceReport) -> None:
        stmt = text(
            """
            DELETE FROM device_reports WHERE report_id = :report_id
            """
        )

        self._connection.execute(stmt, {"report_id": model.entity_id})
