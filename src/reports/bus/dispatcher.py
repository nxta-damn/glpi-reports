from typing import cast

from reports.bus.build_pipelines_chain import build_pipeline_behaviors_chain
from reports.bus.registry import Registry
from reports.bus.resolver import Resolver
from reports.domain.shared.markers import Notification
from reports.presentation.bus_requests_sender import Sender
from reports.services.common.markers import Request
from reports.services.ports.notification_publisher import Publisher


class Dispatcher(Sender, Publisher):
    def __init__(self, resolver: Resolver, registry: Registry) -> None:
        self._resolver = resolver
        self._registry = registry

    def send[TRes](self, request: Request[TRes]) -> TRes:
        request_type = type(request)

        handler_class = self._registry.get_request_handler(request_type)

        if not handler_class:
            raise KeyError(f"Request handler for {request_type} not found")

        handler = self._resolver.resolve(handler_class)
        behaviors = [
            self._resolver.resolve(behavior_type)
            for behavior_type in self._registry.get_pipeline_behaviors(
                request_type,
            )
        ]
        handle_next = build_pipeline_behaviors_chain(handler, behaviors)

        return cast("TRes", handle_next(request))

    def publish(self, notification: Notification) -> None:
        notification_type = type(notification)

        handler_classes = self._registry.get_notification_handlers(
            notification_type,
        )
        for handler_class in handler_classes:
            handler = self._resolver.resolve(handler_class)
            behaviors = [
                self._resolver.resolve(behavior_type)
                for behavior_type in self._registry.get_pipeline_behaviors(
                    notification_type,
                )
            ]
            handle_next = build_pipeline_behaviors_chain(handler, behaviors)

            handle_next(notification)
