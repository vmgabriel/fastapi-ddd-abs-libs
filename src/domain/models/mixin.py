import abc
from typing import Any, List, cast

from src.domain.models import filter, repository
from src.infra.log import model as model_log
from src.infra.uow import model as model_uow


class GetterMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence
    logger: model_log.LogAdapter
    _filter_builder: filter.FilterBuilder

    _session: model_uow.Session
    _equal_id_filter: filter.FilterDefinition

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = cast(
            repository.RepositoryPersistence, kwargs.get("repository_persistence")
        )
        self.logger = cast(model_log.LogAdapter | None, kwargs.get("logger")) or cast(
            model_log.LogAdapter, kwargs.get("log")
        )
        self._filter_builder = cast(filter.FilterBuilder, kwargs.get("filter_builder"))
        self._session = cast(model_uow.Session, kwargs.get("session"))

        self._equal_id_filter = self._filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )("id")

    @abc.abstractmethod
    def serialize(self, data: Any) -> repository.RepositoryData | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: str) -> repository.RepositoryData | None:
        raise NotImplementedError()


class GetterListMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence
    logger: model_log.LogAdapter

    _filter_builder: filter.FilterBuilder
    _session: model_uow.Session

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = cast(
            repository.RepositoryPersistence, kwargs.get("repository_persistence")
        )
        self.logger = cast(model_log.LogAdapter | None, kwargs.get("logger")) or cast(
            model_log.LogAdapter, kwargs.get("log")
        )
        self._filter_builder = cast(filter.FilterBuilder, kwargs.get("filter_builder"))
        self._session = cast(model_uow.Session, kwargs.get("session"))

    @abc.abstractmethod
    def filter(
        self,
        criteria: filter.Criteria,
        custom_filter: repository.CustomQuery | None = None,
        joins: List[filter.Join] | None = None,
    ) -> filter.Paginator:
        raise NotImplementedError()

    @abc.abstractmethod
    def serialize(self, data: Any) -> repository.RepositoryData | None:
        raise NotImplementedError()


class CreatorMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence

    _session: model_uow.Session
    _filter_builder: filter.FilterBuilder
    logger: model_log.LogAdapter

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = cast(
            repository.RepositoryPersistence, kwargs.get("repository_persistence")
        )
        self.logger = cast(model_log.LogAdapter | None, kwargs.get("logger")) or cast(
            model_log.LogAdapter, kwargs.get("log")
        )
        self._filter_builder = cast(filter.FilterBuilder, kwargs.get("filter_builder"))
        self._session = cast(model_uow.Session, kwargs.get("session"))

    @abc.abstractmethod
    def create(self, new: repository.RepositoryData) -> repository.RepositoryData:
        raise NotImplementedError()


class UpdaterMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence

    _session: model_uow.Session
    logger: model_log.LogAdapter
    _filter_builder: filter.FilterBuilder

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = cast(
            repository.RepositoryPersistence, kwargs.get("repository_persistence")
        )
        self.logger = cast(model_log.LogAdapter | None, kwargs.get("logger")) or cast(
            model_log.LogAdapter, kwargs.get("log")
        )
        self._filter_builder = cast(filter.FilterBuilder, kwargs.get("filter_builder"))
        self._session = cast(model_uow.Session, kwargs.get("session"))

    @abc.abstractmethod
    def update(
        self, id: str, to_update: repository.RepositoryData
    ) -> repository.RepositoryData:
        raise NotImplementedError()


class DeleterMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence
    filter_builder: filter.FilterBuilder

    _session: model_uow.Session
    logger: model_log.LogAdapter
    _filter_builder: filter.FilterBuilder

    _equal_id_filter: filter.FilterDefinition

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = cast(
            repository.RepositoryPersistence, kwargs.get("repository_persistence")
        )
        self.logger = cast(model_log.LogAdapter | None, kwargs.get("logger")) or cast(
            model_log.LogAdapter, kwargs.get("log")
        )
        self._filter_builder = cast(filter.FilterBuilder, kwargs.get("filter_builder"))
        self._session = cast(model_uow.Session, kwargs.get("session"))

        self._equal_id_filter = self.filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )("id")

    @abc.abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError()
