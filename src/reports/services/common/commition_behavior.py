from reports.services.common.markers import Command
from reports.services.common.pipeline import HandleNext, PipelineBehavior
from reports.services.ports.transaction import Transaction


class CommitionBehavior[C: Command, R](PipelineBehavior[C, R]):
    def __init__(self, transaction: Transaction) -> None:
        self._transaction = transaction

    def handle(self, request: C, handle_next: HandleNext[C, R]) -> R:
        response = handle_next(request)

        self._transaction.commit()

        return response
