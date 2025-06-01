from uuid_extensions import uuid7
from datetime import datetime, UTC

from sqlalchemy import text, Connection
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from reports.ioc.ioc_containers import ApiContainer


def test_change_report(test_client: TestClient, api_container: ApiContainer) -> None:
    """Test successful update of a device report."""
    # Setup test data
    report_id = uuid7()
    creator_id = uuid7()
    current_date = datetime.now(UTC)

    # Create initial report
    with api_container() as req_container:
        connection = req_container.get(Connection)

        insert_sql = text(
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
            insert_sql,
            {
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

    # Update the report
    update_payload = {
        "report_name": "new report",
        "comment": "new comment",
    }

    result = test_client.put(
        f"/reports/{report_id}",
        json=update_payload,
        headers={"X-User-Id": str(creator_id)}
    )
    assert result.status_code == HTTP_200_OK

    # Verify the changes
    with api_container() as req_container:
        connection = req_container.get(Connection)
        select_sql = text("SELECT * FROM device_reports WHERE report_id = :report_id")
        result = connection.execute(select_sql, {"report_id": report_id})
        row = result.fetchone()

    assert row is not None
    assert row.report_name == update_payload["report_name"]
    assert row.comment == update_payload["comment"]


def test_change_device_with_unauthorized_user(test_client: TestClient) -> None:
    """Test update fails with unauthorized user."""
    report_id = uuid7()
    update_payload = {
        "report_name": "new report",
        "comment": "new comment",
    }

    result = test_client.put(
        f"/reports/{report_id}",
        json=update_payload,
    )

    assert result.status_code == HTTP_401_UNAUTHORIZED


def test_change_device_with_non_existent_report(test_client: TestClient) -> None:
    """Test update fails with non-existent report."""
    update_payload = {
        "report_name": "new report",
        "comment": "new comment",
    }

    result = test_client.put(
        f"/reports/{uuid7()}",
        json=update_payload,
        headers={"X-User-Id": str(uuid7())}
    )

    assert result.status_code == HTTP_404_NOT_FOUND
