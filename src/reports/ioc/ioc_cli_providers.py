from dishka import (
    Provider,
    Scope,
    from_context,
)

from reports.config import CliConfig


class CliConfigProvider(Provider):
    scope = Scope.APP

    cli_config = from_context(provides=CliConfig)
