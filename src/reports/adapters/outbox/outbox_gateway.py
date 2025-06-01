from abc import ABC, abstractmethod

from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.services.models.pagination import Pagination


class OutboxGateway(ABC):
    @abstractmethod
    def load_many(self, pagination: Pagination) -> list[OutboxMessage]: ...
    @abstractmethod
    def add(self, message: OutboxMessage) -> None: ...
    @abstractmethod
    def delete_many(self, messages: list[OutboxMessage]) -> None: ...
