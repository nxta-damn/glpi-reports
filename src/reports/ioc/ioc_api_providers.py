from collections.abc import Iterator

from dishka import Provider, Scope, WithParents, alias, from_context, provide, provide_all
from sqlalchemy import Connection, Engine, create_engine

from reports.adapters.events import DomainEvents
from reports.adapters.outbox.outbox_storing_handler import OutboxStoringHandler
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
from reports.adapters.persistence.adapters.sql_report_gateway import SqlReportGateway
from reports.adapters.persistence.adapters.sql_report_repository import (
    SqlReportRepository,
)
from reports.adapters.persistence.adapters.sql_unit_of_work import UnitOfWorkImpl
from reports.adapters.report_factory import ReportFactoryImlp
from reports.adapters.utc_time_provider import UtcTimeProvider
from reports.adapters.uuid7_id_generator import UUID7IdGenerator
from reports.bus.adapters.dishka_resolver import DishkaResolver
from reports.bus.dispatcher import Dispatcher
from reports.bus.registry import Registry
from reports.config import ApiConfig
from reports.domain.shared.events import DomainEvent
from reports.presentation.api.http_identity_provider import HttpIdentityProvider
from reports.services.common.commition_behavior import CommitionBehavior
from reports.services.common.event_date_setter_behavior import EventDateSetterBehavior
from reports.services.common.event_id_generation_behavior import EventIdGenerationBehavior
from reports.services.common.event_publishing_behavior import EventPublishingBehavior
from reports.services.common.markers import Command
from reports.services.operations.read.load_report_by_id import (
    LoadReportById,
    LoadReportByIdHandler,
)
from reports.services.operations.read.load_reports import LoadReports, LoadReportsHandler
from reports.services.operations.write.add_report import (
    AddDeviceReport,
    AddDeviceReportHandler,
)
from reports.services.operations.write.change_report import (
    ChangeDeviceReport,
    ChangeDeviceReportHandler,
)
from reports.services.operations.write.delete_report import (
    DeleteDeviceReport,
    DeleteDeviceReportHandler,
)
from reports.services.ports.transaction import Transaction


class ApiConfigProvider(Provider):
    scope = Scope.APP

    api_config = from_context(provides=ApiConfig)


class ApiAuthProvider(Provider):
    scope = Scope.REQUEST

    identity_provider = provide(WithParents[HttpIdentityProvider])  # type: ignore[misc]


class ApiPersistenceProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP, provides=Engine)
    def sa_engine(self, config: ApiConfig) -> Iterator[Engine]:
        engine = create_engine(
            url=config.postgres.dsn, pool_size=10, max_overflow=20, pool_recycle=3600
        )
        yield engine
        engine.dispose()

    @provide(provides=Connection)
    def sa_connection(self, engine: Engine) -> Iterator[Connection]:
        with engine.connect() as connection:
            yield connection


class ApiApplicationHandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        LoadReportsHandler,
        LoadReportByIdHandler,
        AddDeviceReportHandler,
        ChangeDeviceReportHandler,
        DeleteDeviceReportHandler,
        OutboxStoringHandler,
    )

    behaviors = provide_all(
        CommitionBehavior,
        EventDateSetterBehavior,
        EventIdGenerationBehavior,
        EventPublishingBehavior,
    )


class ApiBusProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def bus_registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(LoadReportById, LoadReportByIdHandler)
        registry.add_request_handler(LoadReports, LoadReportsHandler)
        registry.add_request_handler(AddDeviceReport, AddDeviceReportHandler)
        registry.add_request_handler(ChangeDeviceReport, ChangeDeviceReportHandler)
        registry.add_request_handler(DeleteDeviceReport, DeleteDeviceReportHandler)
        registry.add_notification_handlers(DomainEvent, OutboxStoringHandler)
        registry.add_pipeline_behaviors(
            DomainEvent, EventDateSetterBehavior, EventIdGenerationBehavior
        )
        registry.add_pipeline_behaviors(
            Command,
            EventPublishingBehavior,
            CommitionBehavior,
        )
        return registry

    resolver = provide(WithParents[DishkaResolver])  # type: ignore[misc]
    dispatcher = provide(WithParents[Dispatcher])  # type: ignore[misc]


class ApiInfrastructureAdaptersProvider(Provider):
    scope = Scope.REQUEST

    data_mappers = provide_all(
        WithParents[SqlDeviceReportDataMapper],  # type: ignore[misc]
        WithParents[SqlOutboxMessageDataMapper],  # type: ignore[misc]
    )

    data_mappers_registry = provide(
        WithParents[SqlDataMappersRegistry],  # type: ignore[misc]
    )

    unit_of_work = provide(WithParents[UnitOfWorkImpl])  # type: ignore[misc]


class ApiApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    gateways = provide_all(
        WithParents[SqlOutboxGateway],  # type: ignore[misc]
        WithParents[SqlReportGateway],  # type: ignore[misc]
    )

    id_generator = provide(WithParents[UUID7IdGenerator], scope=Scope.APP)  # type: ignore[misc]
    time_provider = provide(WithParents[UtcTimeProvider], scope=Scope.APP)  # type: ignore[misc]
    transaction = alias(Connection, provides=Transaction)
    domain_events = provide(WithParents[DomainEvents])  # type: ignore[misc]


class ApiDomainAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(WithParents[SqlReportRepository])  # type: ignore[misc]
    report_factory = provide(WithParents[ReportFactoryImlp])  # type: ignore[misc]
