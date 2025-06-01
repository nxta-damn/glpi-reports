from sqlalchemy import Connection, text

from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.persistence.sql_data_mapper import DataMapper


class SqlOutboxMessageDataMapper(DataMapper[OutboxMessage]):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def insert(self, model: OutboxMessage) -> None:
        stmt = text(
            """
            INSERT INTO outbox (data, event_type, message_id)
            VALUES (:data, :event_type, :message_id)
            """
        )

        self._connection.execute(
            stmt,
            {
                "data": model.data,
                "event_type": model.event_type,
                "message_id": model.message_id,
            },
        )

    def delete(self, model: OutboxMessage) -> None:
        stmt = text(
            """
            DELETE FROM outbox WHERE message_id = :message_id
            """
        )

        self._connection.execute(stmt, {"message_id": model.message_id})

    def update(self, model: OutboxMessage) -> None: ...
