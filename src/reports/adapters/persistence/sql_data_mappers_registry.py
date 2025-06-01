from abc import ABC, abstractmethod

from reports.adapters.persistence.sql_data_mapper import DataMapper


class DataMappersRegistry(ABC):
    @abstractmethod
    def get_mapper[T](self, model: type[T]) -> DataMapper[T]: ...
