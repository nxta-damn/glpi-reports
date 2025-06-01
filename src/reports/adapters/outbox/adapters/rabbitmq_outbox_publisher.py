from enum import StrEnum
from typing import Final

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel as Channel
from pika.exceptions import AMQPError

from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.outbox.outbox_publisher import OutboxPublisher
from reports.adapters.outbox.outbox_serialization import to_json


class ReportsExchange(StrEnum):
    REPORTS = "reports"


def declare_reports_exchange(channel: Channel) -> None:
    channel.exchange_declare(
        exchange=ReportsExchange.REPORTS,
        exchange_type="topic",
        durable=True,
    )


class RabbitOutboxPublisher(OutboxPublisher):
    _CONTENT_TYPE: Final[str] = "application/json"
    _DELIVERY_MODE: Final[int] = 2

    def __init__(self, pika_channel: Channel) -> None:
        self._channel = pika_channel

    def publish(self, messages: list[OutboxMessage]) -> list[OutboxMessage]:
        published_messages: list[OutboxMessage] = []

        for outbox_message in messages:
            try:
                self._publish_message(outbox_message)
                published_messages.append(outbox_message)
            except AMQPError:
                continue

        return published_messages

    def _publish_message(self, message: OutboxMessage) -> None:
        self._channel.confirm_delivery()
        self._channel.basic_publish(
            exchange=ReportsExchange.REPORTS,
            routing_key=message.event_type,
            body=to_json(message).encode(),
            properties=BasicProperties(
                content_type=self._CONTENT_TYPE,
                headers={
                    "X-Content-Type": self._CONTENT_TYPE,
                    "X-Event-Id": str(message.message_id),
                    "X-Event-Type": message.event_type,
                },
                delivery_mode=self._DELIVERY_MODE,
            ),
        )
