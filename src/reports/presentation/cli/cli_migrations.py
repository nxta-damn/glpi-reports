from alembic.command import current as alembic_current
from alembic.command import downgrade as alembic_downgrade
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject

from reports.config import CliConfig


@option(
    "-m",
    "--message",
    default=None,
    help="A message for migration, such as a description of changes",
)
@inject
def make_migrations(
    message: str | None,
    *,
    cli_config: FromDishka[CliConfig],
) -> None:
    alembic_revision(cli_config.alembic, message, autogenerate=True)


@option(
    "-r",
    "--revision",
    default="head",
    help="Revision for applying migration, by default 'head'.",
)
@argument("revision", default="head")
@inject
def upgrade_migration(
    revision: str,
    *,
    cli_config: FromDishka[CliConfig],
) -> None:
    alembic_upgrade(cli_config.alembic, revision)


@option(
    "-r",
    "--revision",
    default="base",
    help="Revision for downgrading migration, by default 'base'.",
)
@argument("revision", default="base")
@inject
def downgrade_migration(
    revision: str,
    *,
    cli_config: FromDishka[CliConfig],
) -> None:
    alembic_downgrade(cli_config.alembic, revision)


@inject
def show_current_migration(*, cli_config: FromDishka[CliConfig]) -> None:
    alembic_current(cli_config.alembic)
