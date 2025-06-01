from sqlalchemy import UUID, Column, DateTime, Integer, MetaData, Table, Text
from sqlalchemy.orm import registry

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)


DEVICE_REPORT_TABLE = Table(
    "device_reports",
    METADATA,
    Column("report_id", UUID, primary_key=True),
    Column("report_name", Text, nullable=False),
    Column("creator_id", UUID, nullable=False),
    Column("comment", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("device_id", Integer, nullable=False),
    Column("device_type", Text, nullable=False),
)

OUTBOX_TABLE = Table(
    "outbox",
    MAPPER_REGISTRY.metadata,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)
