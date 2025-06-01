from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ValueObject):
            return NotImplemented

        return self.__dict__ == value.__dict__

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __repr__(self) -> str:
        return self.__str__()
