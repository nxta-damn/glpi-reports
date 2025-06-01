from abc import ABC, abstractmethod

from reports.domain.shared.markers import Notification
from reports.services.common.markers import Request


class RequestHandler[TReq_contra: Request, TRes_co](ABC):
    @abstractmethod
    def handle(self, request: TReq_contra) -> TRes_co: ...


class NotificationHandler[TNot_contra: Notification](ABC):
    @abstractmethod
    def handle(self, notification: TNot_contra) -> None: ...
