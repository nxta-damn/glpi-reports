from sqlalchemy import Connection, Row, text

from reports.adapters.outbox.outbox_gateway import OutboxGateway
from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.persistence.sql_unit_of_work import UnitOfWork
from reports.services.models.pagination import Pagination


class SqlOutboxGateway(OutboxGateway):
    def __init__(self, connection: Connection, unit_of_work: UnitOfWork) -> None:
        self._connection = connection
        self._unit_of_work = unit_of_work

    def add(self, message: OutboxMessage) -> None:
        self._unit_of_work.register_new(message)

    def delete_many(self, messages: list[OutboxMessage]) -> None:
        for message in messages:
            self._unit_of_work.register_deleted(message)

    def load_many(self, pagination: Pagination) -> list[OutboxMessage]:
        stmt = text(
            """
            SELECT data, event_type, message_id FROM outbox
            LIMIT :limit
            OFFSET :offset
            """
        )
        result = self._connection.execute(
            stmt, {"limit": pagination.limit, "offset": pagination.offset}
        )
        rows = result.fetchall()

        return [self._load(row) for row in rows]

    def _load(self, row: Row) -> OutboxMessage:
        message = OutboxMessage(
            data=row.data, message_id=row.message_id, event_type=row.event_type
        )
        return message
