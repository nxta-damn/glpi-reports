from abc import ABC, abstractmethod

from reports.adapters.outbox.outbox_message import OutboxMessage


class OutboxPublisher(ABC):
    @abstractmethod
    def publish(self, messages: list[OutboxMessage]) -> list[OutboxMessage]: ...
