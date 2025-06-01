from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.persistence.sql_tables import (
    DEVICE_REPORT_TABLE,
    MAPPER_REGISTRY,
    OUTBOX_TABLE,
)
from reports.domain.report.report import DeviceReport


def map_device_report_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        DeviceReport,
        DEVICE_REPORT_TABLE,
        properties={
            "_entity_id": DEVICE_REPORT_TABLE.c.report_id,
            "_report_name": DEVICE_REPORT_TABLE.c.report_name,
            "_creator_id": DEVICE_REPORT_TABLE.c.creator_id,
            "_comment": DEVICE_REPORT_TABLE.c.comment,
            "_created_at": DEVICE_REPORT_TABLE.c.created_at,
            "_device_id": DEVICE_REPORT_TABLE.c.device_id,
            "_device_type": DEVICE_REPORT_TABLE.c.device_type,
        },
    )


def map_outbox_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        OutboxMessage,
        OUTBOX_TABLE,
        properties={
            "_data": OUTBOX_TABLE.c.data,
            "_event_type": OUTBOX_TABLE.c.event_type,
            "_message_id": OUTBOX_TABLE.c.message_id,
        },
    )


def map_tables() -> None:
    if not hasattr(DeviceReport, "__mapper__"):
        map_device_report_table()

    if not hasattr(OutboxMessage, "__mapper__"):
        map_outbox_table()
