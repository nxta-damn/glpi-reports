from reports.services.common.markers import Command
from reports.services.common.pipeline import HandleNext, PipelineBehavior
from reports.services.ports.events import DomainEventsRaiser
from reports.services.ports.notification_publisher import Publisher


class EventPublishingBehavior[C: Command, R](PipelineBehavior[C, R]):
    def __init__(
        self,
        publisher: Publisher,
        events_raiser: DomainEventsRaiser,
    ) -> None:
        self._publisher = publisher
        self._events_raiser = events_raiser

    def handle(self, request: C, handle_next: HandleNext[C, R]) -> R:
        response = handle_next(request)

        for event in self._events_raiser.raise_events():
            self._publisher.publish(event)

        return response
