from uuid import UUID

from reports.adapters.outbox.outbox_gateway import OutboxGateway
from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.outbox.outbox_serialization import to_json
from reports.domain.shared.events import DomainEvent
from reports.services.common.handlers import NotificationHandler


class OutboxStoringHandler(NotificationHandler[DomainEvent]):
    def __init__(self, outbox_gateway: OutboxGateway) -> None:
        self._outbox_gateway = outbox_gateway

    def handle(self, notification: DomainEvent) -> None:
        message = OutboxMessage(
            data=to_json(notification),
            message_id=UUID(str(notification.event_id)),
            event_type=notification.event_type,
        )

        self._outbox_gateway.add(message)
