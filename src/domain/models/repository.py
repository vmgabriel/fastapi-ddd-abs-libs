import abc
import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

import pydantic

from src import settings
from src.domain import libtools
from src.infra.log import model as log_model

T = TypeVar("T", bound="Repository")


class RepositoryHasAlreadyExistsError(Exception):
    message: str = "Repository has Already Exists"


class RepositoryNotFoundError(Exception):
    message: str = "Repository Not Found"


class PersistenceTypeNotFoundError(Exception):
    message: str = "Persistence Not Found"


class RepositoryData(pydantic.BaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None
    is_activated: bool = True


class RepositoryPersistence(pydantic.BaseModel):
    table_name: str
    fields: List[str]


class Repository(abc.ABC):
    log: log_model.LogAdapter
    configuration: settings.BaseSettings
    persistence: RepositoryPersistence

    _data: RepositoryData | None

    def __init__(
        self,
        configuration: settings.BaseSettings,
        persistence: RepositoryPersistence,
        log: log_model.LogAdapter,
    ) -> None:
        self.configuration = configuration
        self.persistence = persistence
        self.log = log
        self._data = None

    @abc.abstractmethod
    def serialize(self, data: Any) -> "Repository":
        raise NotImplementedError()

    @abc.abstractmethod
    def dict(self) -> Dict[str, Any] | None:
        raise NotImplementedError()

    def repository_name(self) -> str:
        return self.__class__.__name__


class RepositoryGetter:
    repositories: Dict[Type[Repository], Type[Repository]]

    def __init__(self, repositories: List[Type[Repository]] | None = None) -> None:
        self.repositories = {}
        for repository in repositories or []:
            parent_repository = [
                mro_class
                for mro_class in libtools.get_mro_class(repository)
                if "Repository" in mro_class.__name__
            ]
            if not parent_repository or len(parent_repository) <= 2:
                raise PersistenceTypeNotFoundError(
                    f"Persistence Type Not Found for {repository.__name__}"
                )
            self.repositories[cast(Type[Repository], parent_repository[1])] = repository

    def __add__(self, other: "RepositoryGetter") -> "RepositoryGetter":
        self.repositories.update(other.repositories)
        return self
