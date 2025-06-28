import abc
from typing import Any

from src.domain.models import filter, repository
from src.infra.log import model as model_log
from src.infra.uow import model as model_uow


class GetterMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence
    logger: model_log.LogAdapter
    filter_builder: filter.FilterBuilder

    _session: model_uow.Session
    _equal_id_filter: filter.FilterDefinition

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = kwargs.get("repository_persistence")
        self.logger = kwargs.get("logger") or kwargs.get("log")
        self.filter_builder = kwargs.get("filter_builder")
        self._session = kwargs.get("session")

        self._equal_id_filter = self.filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )("id")

    @abc.abstractmethod
    def serialize(self, data: Any) -> repository.Repository:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: str):
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
        self.repository_persistence = kwargs.get("repository_persistence")
        self.logger = kwargs.get("logger") or kwargs.get("log")
        self.filter_builder = kwargs.get("filter_builder")
        self._session = kwargs.get("session")

    @abc.abstractmethod
    def filter(self, criteria: filter.Criteria) -> filter.Paginator:
        raise NotImplementedError()

    @abc.abstractmethod
    def serialize(self, data: Any) -> repository.Repository:
        raise NotImplementedError()


class CreatorMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence

    _session: model_uow.Session
    logger: model_log.LogAdapter

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = kwargs.get("repository_persistence")
        self.logger = kwargs.get("logger") or kwargs.get("log")
        self.filter_builder = kwargs.get("filter_builder")
        self._session = kwargs.get("session")

    @abc.abstractmethod
    def create(self, new: repository.RepositoryData) -> repository.RepositoryData:
        raise NotImplementedError()


class UpdaterMixin(abc.ABC):
    repository_persistence: repository.RepositoryPersistence

    _session: model_uow.Session
    logger: model_log.LogAdapter

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = kwargs.get("repository_persistence")
        self.logger = kwargs.get("logger") or kwargs.get("log")
        self.filter_builder = kwargs.get("filter_builder")
        self._session = kwargs.get("session")

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

    _equal_id_filter: filter.FilterDefinition

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.repository_persistence = kwargs.get("repository_persistence")
        self.logger = kwargs.get("logger") or kwargs.get("log")
        self.filter_builder = kwargs.get("filter_builder")
        self._session = kwargs.get("session")

        self._equal_id_filter = self.filter_builder.build(
            type_filter=filter.FilterType.EQUAL
        )("id")

    @abc.abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError()
