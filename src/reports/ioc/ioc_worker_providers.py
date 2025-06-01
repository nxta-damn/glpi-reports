from collections.abc import Iterator

from dishka import Provider, Scope, WithParents, alias, from_context, provide, provide_all
from pika import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from sqlalchemy import Connection, Engine, create_engine

from reports.adapters.outbox.adapters.rabbitmq_outbox_publisher import (
    RabbitOutboxPublisher,
)
from reports.adapters.outbox.outbox_processor import OutboxProcessor
from reports.adapters.persistence.adapters.sql_data_mappers_registry import (
    SqlDataMappersRegistry,
)
from reports.adapters.persistence.adapters.sql_outbox_gateway import SqlOutboxGateway
from reports.adapters.persistence.adapters.sql_outbox_message_data_mapper import (
    SqlOutboxMessageDataMapper,
)
from reports.adapters.persistence.adapters.sql_report_data_mapper import (
    SqlDeviceReportDataMapper,
)
from reports.adapters.persistence.adapters.sql_unit_of_work import UnitOfWorkImpl
from reports.config import WorkerConfig
from reports.services.ports.transaction import Transaction


class WorkerConfigProvider(Provider):
    scope = Scope.APP

    worker_config = from_context(provides=WorkerConfig)


class WorkerPersistenceProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP, provides=Engine)
    def sa_engine(self, config: WorkerConfig) -> Iterator[Engine]:
        engine = create_engine(url=config.postgres.dsn)
        yield engine
        engine.dispose()

    @provide
    def sa_connection(self, engine: Engine) -> Iterator[Connection]:
        with engine.connect() as connection:
            yield connection


class WorkerInfrastructureAdaptersProvider(Provider):
    scope = Scope.REQUEST

    data_mappers = provide_all(
        WithParents[SqlDeviceReportDataMapper],  # type: ignore[misc]
        WithParents[SqlOutboxMessageDataMapper],  # type: ignore[misc]
    )

    data_mappers_registry = provide(
        WithParents[SqlDataMappersRegistry],  # type: ignore[misc]
    )

    unit_of_work = provide(WithParents[UnitOfWorkImpl])  # type: ignore[misc]


class WorkerApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    gateways = provide_all(
        WithParents[SqlOutboxGateway],  # type: ignore[misc]
    )

    transaction = alias(Connection, provides=Transaction)
    outbox_processor = provide(OutboxProcessor)


class WorkerBrokerProvider(Provider):
    scope = Scope.REQUEST

    outbox_publisher = provide(WithParents[RabbitOutboxPublisher])  # type: ignore[misc]

    @provide(scope=Scope.APP, provides=BlockingConnection)
    def rabbit_connection(self, config: WorkerConfig) -> Iterator[BlockingConnection]:
        connection = BlockingConnection(parameters=URLParameters(url=config.rabbit.dsn))
        yield connection

    @provide(provides=BlockingChannel)
    def rabbit_channel(self, connection: BlockingConnection) -> Iterator[BlockingChannel]:
        channel = connection.channel()
        yield channel
