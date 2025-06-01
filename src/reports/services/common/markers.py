from dataclasses import dataclass


class Request[TRes]: ...


@dataclass(frozen=True)
class Command[TRes](Request[TRes]): ...


@dataclass(frozen=True)
class Query[TRes](Request[TRes]): ...
