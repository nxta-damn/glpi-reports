from typing import Any

from sqlalchemy import Connection

from reports.adapters.persistence.sql_data_mappers_registry import DataMappersRegistry
from reports.adapters.persistence.sql_unit_of_work import UnitOfWork
from reports.services.ports.transaction import Transaction


class UnitOfWorkImpl(UnitOfWork, Transaction):
    def __init__(
        self, connection: Connection, data_mappers_registry: DataMappersRegistry
    ) -> None:
        self._connection = connection
        self._data_mappers_registry = data_mappers_registry
        self._new_models: list[Any] = []
        self._dirty_models: list[Any] = []
        self._deleted_models: list[Any] = []

    def register_new(self, model: Any) -> None:
        self._new_models.append(model)

    def register_dirty(self, model: Any) -> None:
        self._dirty_models.append(model)

    def register_deleted(self, model: Any) -> None:
        self._deleted_models.append(model)

    def commit(self) -> None:
        for model in self._new_models:
            mapper = self._data_mappers_registry.get_mapper(type(model))
            mapper.insert(model)

        for model in self._dirty_models:
            mapper = self._data_mappers_registry.get_mapper(type(model))
            mapper.update(model)

        for model in self._deleted_models:
            mapper = self._data_mappers_registry.get_mapper(type(model))
            mapper.delete(model)

        self._connection.commit()
        self._new_models.clear()
        self._dirty_models.clear()
        self._deleted_models.clear()
