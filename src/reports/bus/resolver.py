from abc import ABC, abstractmethod


class Resolver(ABC):
    @abstractmethod
    def resolve[T](self, dependency_type: type[T]) -> T: ...
