from abc import ABC, abstractmethod
from typing import Any


class UnitOfWork(ABC):
    @abstractmethod
    def register_new(self, model: Any) -> None: ...
    @abstractmethod
    def register_dirty(self, model: Any) -> None: ...
    @abstractmethod
    def register_deleted(self, model: Any) -> None: ...
