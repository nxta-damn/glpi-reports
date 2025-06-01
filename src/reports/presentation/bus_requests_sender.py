from abc import ABC, abstractmethod

from reports.services.common.markers import Request


class Sender(ABC):
    @abstractmethod
    def send[TRes](self, request: Request[TRes]) -> TRes: ...
