from uuid import UUID


class OutboxMessage:
    def __init__(self, data: str | bytes, event_type: str, message_id: UUID) -> None:
        self._data = data
        self._event_type = event_type
        self._message_id = message_id

    @property
    def data(self) -> str | bytes:
        return self._data

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def message_id(self) -> UUID:
        return self._message_id

    def __str__(self) -> str:
        return f"OutboxMessage({self._data!r}, {self._event_type}, {self._message_id})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OutboxMessage):
            return False

        return (
            self._event_type == other.event_type and self._message_id == other.message_id
        )

    def __hash__(self) -> int:
        return hash(self._message_id)
