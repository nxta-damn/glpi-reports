from collections.abc import AsyncGenerator

from dishka import Container
from hatchet_sdk import Worker
from hatchet_sdk.config import ClientConfig
from pika.adapters.blocking_connection import BlockingChannel as Channel
from pydantic import BaseModel, ConfigDict

from reports.adapters.outbox.adapters.rabbitmq_outbox_publisher import (
    declare_reports_exchange,
)
from reports.adapters.outbox.outbox_workflow import OUTBOX_WORKFLOW
from reports.adapters.persistence.sql_mappings import map_tables
from reports.config import WorkerConfig
from reports.ioc.ioc_containers import bootstrap_worker_container


class Lifespan(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dishka_container: Container


async def lifespan() -> AsyncGenerator[Lifespan, None]:
    map_tables()
    config = WorkerConfig()
    dishka_container = bootstrap_worker_container(config=config)

    with dishka_container() as req_container:
        pika_channel = req_container.get(Channel)
        declare_reports_exchange(channel=pika_channel)

    with dishka_container() as scoped_container:
        yield Lifespan(dishka_container=scoped_container)


def get_hathcet_app() -> Worker:
    config = WorkerConfig()

    worker = Worker(
        name="ReportsWorker",
        lifespan=lifespan,
        config=ClientConfig(token=config.hatchet.api_key),
        slots=5,
        durable_slots=20,
        workflows=[OUTBOX_WORKFLOW],
    )

    return worker
