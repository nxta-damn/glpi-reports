from uuid_extensions import uuid7
from datetime import datetime, UTC

from sqlalchemy import text, Connection
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from reports.ioc.ioc_containers import ApiContainer


def test_delete_report(test_client: TestClient, api_container: ApiContainer) -> None:
    """Test successful deletion of a device report."""
    report_id = uuid7()
    creator_id = uuid7()
    current_date = datetime.now(UTC)

    # Create test report
    with api_container() as req_container:
        connection = req_container.get(Connection)

        stmt = text(
            """
            INSERT INTO device_reports
            (report_id, creator_id, created_at, comment,
            report_name, device_id, device_type)
            VALUES
            (:report_id, :creator_id, :created_at, :comment,
            :report_name, :device_id, :device_type)
            """
        )

        connection.execute(
            stmt, {
                "report_id": report_id,
                "creator_id": creator_id,
                "created_at": current_date,
                "comment": "test",
                "report_name": "test",
                "device_id": 1,
                "device_type": "test",
            }
        )
        connection.commit()

    # Delete the report
    result = test_client.delete(
        f"/reports/{report_id}",
        headers={"X-User-Id": str(creator_id)}
    )
    assert result.status_code == HTTP_200_OK

    # Verify report was deleted
    with api_container() as req_container:
        connection = req_container.get(Connection)
        stmt = text("SELECT * FROM device_reports WHERE report_id = :report_id")
        result = connection.execute(stmt, {"report_id": report_id})
        row = result.fetchone()

    assert row is None


def test_delete_report_with_unauthorized_user(test_client: TestClient) -> None:
    """Test deletion fails with unauthorized user."""
    report_id = uuid7()
    result = test_client.delete(f"/reports/{report_id}")
    assert result.status_code == HTTP_401_UNAUTHORIZED


def test_delete_report_with_non_existent_report(test_client: TestClient) -> None:
    """Test deletion fails with non-existent report."""
    result = test_client.delete(
        f"/reports/{uuid7()}",
        headers={"X-User-Id": str(uuid7())}
    )
    assert result.status_code == HTTP_404_NOT_FOUND
