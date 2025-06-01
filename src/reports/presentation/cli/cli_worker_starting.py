import asyncio
from signal import SIGINT, signal
from types import FunctionType

from click import argument
from dishka import FromDishka
from dishka.integrations.click import inject
from hatchet_sdk import Worker

from reports.config import CliConfig
from reports.presentation.cli.cli_object_imports import import_object


def load_worker(path: str) -> Worker:
    worker_obj = import_object(path)

    if isinstance(worker_obj, Worker):
        return worker_obj

    if isinstance(worker_obj, FunctionType):
        worker_instance = worker_obj()
        if not isinstance(worker_instance, Worker):
            raise TypeError("Worker factory function must return a Worker instance")
        return worker_instance

    raise TypeError("Worker must be a Worker instance or a factory function")


@argument("path", default=None, required=False)
@inject
def start_worker(
    path: str | None,
    *,
    cli_config: FromDishka[CliConfig],
) -> None:
    if path is not None:
        cli_config.worker.app_path = path

    worker = load_worker(cli_config.worker.app_path)
    signal(SIGINT, lambda *_: asyncio.create_task(worker.exit_gracefully()))
    worker.start()
