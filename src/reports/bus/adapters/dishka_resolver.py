from dishka import Container

from reports.bus.resolver import Resolver


class DishkaResolver(Resolver):
    def __init__(self, container: Container) -> None:
        self._container = container

    def resolve[T](self, dependency_type: type[T]) -> T:
        return self._container.get(dependency_type)
