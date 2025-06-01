from dishka import Container, make_container
from dishka.integrations.fastapi import FastapiProvider

from reports.config import ApiConfig, CliConfig, WorkerConfig
from reports.ioc.ioc_api_providers import (
    ApiApplicationAdaptersProvider,
    ApiApplicationHandlersProvider,
    ApiAuthProvider,
    ApiBusProvider,
    ApiConfigProvider,
    ApiDomainAdaptersProvider,
    ApiInfrastructureAdaptersProvider,
    ApiPersistenceProvider,
)
from reports.ioc.ioc_cli_providers import CliConfigProvider
from reports.ioc.ioc_worker_providers import (
    WorkerApplicationAdaptersProvider,
    WorkerBrokerProvider,
    WorkerConfigProvider,
    WorkerInfrastructureAdaptersProvider,
    WorkerPersistenceProvider,
)

type WorkerContainer = Container
type ApiContainer = Container
type CliContainer = Container


def bootstrap_api_container(config: ApiConfig) -> ApiContainer:
    return make_container(
        FastapiProvider(),
        ApiConfigProvider(),
        ApiAuthProvider(),
        ApiPersistenceProvider(),
        ApiApplicationHandlersProvider(),
        ApiBusProvider(),
        ApiApplicationAdaptersProvider(),
        ApiDomainAdaptersProvider(),
        ApiInfrastructureAdaptersProvider(),
        context={ApiConfig: config},
    )


def bootstrap_worker_container(config: WorkerConfig) -> WorkerContainer:
    return make_container(
        WorkerConfigProvider(),
        WorkerPersistenceProvider(),
        WorkerApplicationAdaptersProvider(),
        WorkerBrokerProvider(),
        WorkerInfrastructureAdaptersProvider(),
        context={WorkerConfig: config},
    )


def bootstrap_cli_container(config: CliConfig) -> CliContainer:
    return make_container(CliConfigProvider(), context={CliConfig: config})
