from typing import TYPE_CHECKING, cast

from dishka.integrations.fastapi import setup_dishka as add_container_to_fastapi
from fastapi import FastAPI

from reports.adapters.persistence.sql_mappings import map_tables
from reports.config import ApiConfig
from reports.ioc.ioc_containers import bootstrap_api_container
from reports.presentation.api.exception_handlers import (
    application_error_handler,
    internal_error_handler,
)
from reports.presentation.api.http_healthcheck_controller import HEALTHCHECK_ROUTER
from reports.presentation.api.http_report_controllers import REPORTS_ROUTER
from reports.services.common.application_error import ApplicationError

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    config = ApiConfig()

    app.include_router(REPORTS_ROUTER)
    app.include_router(HEALTHCHECK_ROUTER)
    app.add_exception_handler(
        ApplicationError,
        cast("HTTPExceptionHandler", application_error_handler),
    )
    app.add_exception_handler(
        Exception,
        cast("HTTPExceptionHandler", internal_error_handler),
    )

    container = bootstrap_api_container(config=config)
    add_container_to_fastapi(container, app)
    map_tables()

    return app
