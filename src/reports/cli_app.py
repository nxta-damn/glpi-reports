from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka

from reports.config import CliConfig
from reports.ioc.ioc_containers import bootstrap_cli_container
from reports.presentation.cli.cli_migrations import (
    downgrade_migration,
    make_migrations,
    show_current_migration,
    upgrade_migration,
)
from reports.presentation.cli.cli_server_starting import start_uvicorn
from reports.presentation.cli.cli_worker_starting import start_worker


@group()
@pass_context
def main(context: Context) -> None:
    config = CliConfig()
    dishka_container = bootstrap_cli_container(config=config)
    setup_dishka(dishka_container, context, finalize_container=True)


main.command(start_uvicorn)
main.command(make_migrations)
main.command(upgrade_migration)
main.command(downgrade_migration)
main.command(show_current_migration)
main.command(start_worker)
