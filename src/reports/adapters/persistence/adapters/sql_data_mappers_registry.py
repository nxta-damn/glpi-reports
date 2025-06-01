from reports.adapters.outbox.outbox_message import OutboxMessage
from reports.adapters.persistence.adapters.sql_outbox_message_data_mapper import (
    SqlOutboxMessageDataMapper,
)
from reports.adapters.persistence.adapters.sql_report_data_mapper import (
    SqlDeviceReportDataMapper,
)
from reports.adapters.persistence.sql_data_mapper import DataMapper
from reports.adapters.persistence.sql_data_mappers_registry import DataMappersRegistry
from reports.domain.report.report import DeviceReport


class SqlDataMappersRegistry(DataMappersRegistry):
    def __init__(
        self,
        report_data_mapper: SqlDeviceReportDataMapper,
        outbox_message_data_mapper: SqlOutboxMessageDataMapper,
    ) -> None:
        self._data_mappers_map: dict[type, DataMapper] = {
            DeviceReport: report_data_mapper,
            OutboxMessage: outbox_message_data_mapper,
        }

    def get_mapper[T](self, model: type[T]) -> DataMapper[T]:
        mapper = self._data_mappers_map.get(model)

        if not mapper:
            raise KeyError

        return mapper
