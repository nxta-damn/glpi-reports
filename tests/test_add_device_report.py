from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import Connection, text
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from uuid_extensions import uuid7

from reports.domain.types import ReportId
from reports.ioc.ioc_containers import ApiContainer


def test_add_report(test_client: TestClient, api_container: ApiContainer) -> None:
    """Test successful creation of a device report."""
    # Setup test data
    name = "test report"
    comment = "test comment"
    device_id = 1
    device_type = "Computer"
    creator_id = uuid7()

    # Create the report
    report_data = {
        "report_name": name,
        "comment": comment,
        "device_id": device_id,
        "device_type": device_type,
    }

    response = test_client.post(
        "/reports", json=report_data, headers={"X-User-Id": str(creator_id)}
    )

    # Verify response
    assert response.status_code == HTTP_201_CREATED
    report_id = ReportId(UUID(response.json()["result"]))

    # Verify database record
    with api_container() as req_container:
        connection = req_container.get(Connection)
        select_sql = text("SELECT * FROM device_reports WHERE report_id = :report_id")
        result = connection.execute(select_sql, {"report_id": report_id})
        row = result.fetchone()

    assert row is not None
    assert row.report_name == name
    assert row.comment == comment
    assert row.device_id == device_id
    assert row.device_type == device_type


def test_add_report_with_unauthorized_user(test_client: TestClient) -> None:
    """Test report creation fails with unauthorized user."""
    report_data = {
        "report_name": "test report",
        "comment": "test comment",
        "device_id": 1,
        "device_type": "Computer",
    }

    result = test_client.post("/reports", json=report_data)

    assert result.status_code == HTTP_401_UNAUTHORIZED
