from dataclasses import dataclass
from datetime import datetime

from reports.domain.types import DeviceId, DeviceType, ReportId, UserId


@dataclass(frozen=True)
class ReportReadModel:
    report_id: ReportId
    creator_id: UserId
    comment: str
    created_at: datetime
    report_name: str
    device_id: DeviceId
    device_type: DeviceType
