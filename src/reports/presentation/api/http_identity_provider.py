from typing import Final
from uuid import UUID

from fastapi import Request

from reports.domain.types import UserId
from reports.services.common.application_error import ApplicationError, ErrorType
from reports.services.ports.identity_provider import IdentityProvider


class HttpIdentityProvider(IdentityProvider):
    _USER_ID_HEADER: Final[str] = "X-User-Id"

    def __init__(self, request: Request) -> None:
        self._request = request

    def current_user_id(self) -> UserId:
        user_id = self._request.headers.get(self._USER_ID_HEADER)

        if user_id is None:
            raise ApplicationError(
                message="User id not found in request headers",
                error_type=ErrorType.UNAUTHORIZED,
            )

        try:
            return UserId(UUID(user_id))
        except ValueError as ex:
            raise ApplicationError(
                message="User id is not a valid UUID",
                error_type=ErrorType.UNAUTHORIZED,
            ) from ex
