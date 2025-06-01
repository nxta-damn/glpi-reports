from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync as inject
from fastapi import APIRouter, Body, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from reports.domain.types import ReportId
from reports.presentation.api.http_response_models import ErrorResponse, SuccessResponse
from reports.presentation.bus_requests_sender import Sender
from reports.services.common.application_error import ApplicationError
from reports.services.models.pagination import Pagination
from reports.services.models.report import ReportReadModel
from reports.services.operations.read.load_report_by_id import LoadReportById
from reports.services.operations.read.load_reports import LoadReports
from reports.services.operations.write.add_report import AddDeviceReport
from reports.services.operations.write.change_report import ChangeDeviceReport
from reports.services.operations.write.delete_report import DeleteDeviceReport

REPORTS_ROUTER = APIRouter(prefix="/reports", tags=["Reports"])


@REPORTS_ROUTER.post(
    path="/",
    responses={
        HTTP_201_CREATED: {"model": SuccessResponse[ReportId]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_201_CREATED,
)
@inject
def add_report(
    request: AddDeviceReport, *, sender: FromDishka[Sender]
) -> SuccessResponse[ReportId]:
    report_id = sender.send(request=request)
    return SuccessResponse(status=HTTP_201_CREATED, result=report_id)


@REPORTS_ROUTER.put(
    path="/{report_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
def change_report(
    report_id: ReportId,
    comment: Annotated[str, Body()],
    report_name: Annotated[str, Body()],
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    sender.send(
        request=ChangeDeviceReport(
            report_id=report_id, comment=comment, report_name=report_name
        )
    )
    return SuccessResponse(status=HTTP_200_OK, result=None)


@REPORTS_ROUTER.delete(
    path="/{report_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
def delete_report(
    report_id: ReportId, *, sender: FromDishka[Sender]
) -> SuccessResponse[None]:
    sender.send(request=DeleteDeviceReport(report_id=report_id))
    return SuccessResponse(status=HTTP_200_OK, result=None)


@REPORTS_ROUTER.get(
    path="/",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[list[ReportReadModel]]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
def load_reports(
    pagination: Annotated[Pagination, Depends()], *, sender: FromDishka[Sender]
) -> SuccessResponse[list[ReportReadModel]]:
    reports = sender.send(request=LoadReports(pagination=pagination))
    return SuccessResponse(status=HTTP_200_OK, result=reports)


@REPORTS_ROUTER.get(
    path="/{report_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[ReportReadModel]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
def load_report_by_id(
    report_id: ReportId, *, sender: FromDishka[Sender]
) -> SuccessResponse[ReportReadModel]:
    report = sender.send(request=LoadReportById(report_id=report_id))
    return SuccessResponse(status=HTTP_200_OK, result=report)
