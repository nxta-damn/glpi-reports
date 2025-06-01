from abc import ABC, abstractmethod


class DataMapper[T](ABC):
    @abstractmethod
    def insert(self, model: T) -> None: ...
    @abstractmethod
    def update(self, model: T) -> None: ...
    @abstractmethod
    def delete(self, model: T) -> None: ...
