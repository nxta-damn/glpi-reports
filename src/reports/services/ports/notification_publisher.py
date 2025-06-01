from typing import Protocol

from reports.domain.shared.markers import Notification


class Publisher(Protocol):
    def publish(self, notification: Notification) -> None: ...
