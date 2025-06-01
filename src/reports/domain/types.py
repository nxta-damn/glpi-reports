from typing import NewType
from uuid import UUID

DeviceId = NewType("DeviceId", int)

DeviceType = NewType("DeviceType", str)

ReportId = NewType("ReportId", UUID)

UserId = NewType("UserId", UUID)

EventId = NewType("EventId", UUID)
