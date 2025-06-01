from typing import TYPE_CHECKING, Any, cast

from hatchet_sdk import Context

from reports.adapters.outbox.outbox_processor import OutboxProcessor
from reports.adapters.worker import HATCHET

if TYPE_CHECKING:
    from dishka import Container


OUTBOX_WORKFLOW = HATCHET.workflow(
    name="outbox", description="Outbox workflow", on_crons=["*/1 * * * *"]
)


@OUTBOX_WORKFLOW.task(retries=3, name="publish_events")
def publish_outbox_events(_: Any, ctx: Context) -> None:
    container = cast("Container", ctx.lifespan.dishka_container)
    outbox_processor = container.get(OutboxProcessor)

    outbox_processor.process()
