from collections.abc import Iterator
from typing import TYPE_CHECKING, cast

import pytest
from dishka.integrations.fastapi import setup_dishka as add_container_to_fastapi
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine

from reports.adapters.persistence.sql_mappings import map_tables
from reports.adapters.persistence.sql_tables import METADATA
from reports.ioc.ioc_containers import ApiContainer, bootstrap_api_container
from reports.presentation.api.exception_handlers import (
    application_error_handler,
    internal_error_handler,
)
from reports.presentation.api.http_report_controllers import REPORTS_ROUTER
from reports.services.common.application_error import ApplicationError
from tests.config import ApiTestConfig

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler

    from reports.config import ApiConfig


@pytest.fixture(scope="session")
def api_config() -> ApiTestConfig:
    return ApiTestConfig()


@pytest.fixture(scope="session")
def api_container(api_config: ApiTestConfig) -> ApiContainer:
    return bootstrap_api_container(config=cast("ApiConfig", api_config))


@pytest.fixture(scope="session")
def fastapi_app(api_container: ApiContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(REPORTS_ROUTER)
    app.add_exception_handler(
        Exception, cast("HTTPExceptionHandler", internal_error_handler)
    )
    app.add_exception_handler(
        ApplicationError, cast("HTTPExceptionHandler", application_error_handler)
    )

    with (api_container.get(Engine)).begin() as conn:
        METADATA.drop_all(bind=conn)
        METADATA.create_all(bind=conn)

    map_tables()
    add_container_to_fastapi(api_container, app)
    return app


@pytest.fixture(scope="session")
def test_client(fastapi_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(fastapi_app) as client:
        yield client
