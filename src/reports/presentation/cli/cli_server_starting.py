from signal import SIGINT, signal

from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject
from uvicorn import Config, Server

from reports.config import CliConfig


@argument("path", default=None, required=False)
@option("-h", "--host", default=None, help="The server host")
@option("-p", "--port", default=None, type=int, help="The server port")
@inject
def start_uvicorn(
    path: str | None,
    host: str | None,
    port: int | None,
    *,
    cli_config: FromDishka[CliConfig],
) -> None:
    if path is not None:
        cli_config.uvicorn.app_path = path

    if host is not None:
        cli_config.uvicorn.server_host = host

    if port is not None:
        cli_config.uvicorn.server_port = port

    uvicorn_server = Server(
        config=Config(
            app=cli_config.uvicorn.app_path,
            host=cli_config.uvicorn.server_host,
            port=cli_config.uvicorn.server_port,
        )
    )

    signal(SIGINT, lambda *_: uvicorn_server.handle_exit(sig=SIGINT, frame=None))

    uvicorn_server.run()
