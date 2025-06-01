from reports.domain.shared.events import DomainEvent
from reports.services.common.pipeline import HandleNext, PipelineBehavior
from reports.services.ports.time_provider import TimeProvider


class EventDateSetterBehavior(PipelineBehavior[DomainEvent, None]):
    def __init__(self, time_provider: TimeProvider) -> None:
        self._time_provider = time_provider

    def handle(
        self,
        request: DomainEvent,
        handle_next: HandleNext[DomainEvent, None],
    ) -> None:
        request.set_event_date(
            self._time_provider.current(),
        )

        return handle_next(request)
