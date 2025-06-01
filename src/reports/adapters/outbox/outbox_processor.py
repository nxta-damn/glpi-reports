from collections.abc import Iterator

from reports.adapters.outbox.outbox_gateway import OutboxGateway
from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.outbox.outbox_publisher import OutboxPublisher
from reports.services.models.pagination import Pagination
from reports.services.ports.transaction import Transaction


class OutboxProcessor:
    def __init__(
        self,
        transaction: Transaction,
        outbox_gateway: OutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> None:
        self._transaction = transaction
        self._outbox_gateway = outbox_gateway
        self._outbox_publisher = outbox_publisher

    def process(self) -> None:
        for batch in self._load_in_batches():
            published_messages = self._outbox_publisher.publish(messages=batch)

            if published_messages:
                self._outbox_gateway.delete_many(messages=published_messages)

        self._transaction.commit()

    def _load_in_batches(self, limit: int = 100) -> Iterator[list[OutboxMessage]]:
        offset: int = 0
        while batch := self._outbox_gateway.load_many(
            pagination=Pagination(limit=limit, offset=offset)
        ):
            yield batch
            offset += limit
