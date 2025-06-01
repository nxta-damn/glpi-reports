from reports.domain.shared.events import DomainEvent
from reports.services.common.pipeline import HandleNext, PipelineBehavior
from reports.services.ports.id_generator import IdGenerator


class EventIdGenerationBehavior(PipelineBehavior[DomainEvent, None]):
    def __init__(self, id_generator: IdGenerator) -> None:
        self._id_generator = id_generator

    def handle(
        self,
        request: DomainEvent,
        handle_next: HandleNext[DomainEvent, None],
    ) -> None:
        request.set_event_id(
            self._id_generator.event_id(),
        )

        return handle_next(request)
