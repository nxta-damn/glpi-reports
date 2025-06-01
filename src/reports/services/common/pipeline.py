from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

TRes = TypeVar("TRes")
TRequest = TypeVar("TRequest")


type HandleNext[TReq, TResult] = Callable[[TReq], TResult]


class PipelineBehavior(Generic[TRequest, TRes], ABC):
    @abstractmethod
    def handle(
        self,
        request: TRequest,
        handle_next: HandleNext[TRequest, TRes],
    ) -> TRes: ...
