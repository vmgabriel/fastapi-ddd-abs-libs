import abc
import datetime
from typing import Any, Dict, List

import pydantic

from src import settings
from src.infra.log import model as log_model


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

    def __init__(
        self,
        configuration: settings.BaseSettings,
        persistence: RepositoryPersistence,
        log: log_model.LogAdapter,
    ) -> None:
        self.configuration = configuration
        self.persistence = persistence
        self.log = log

    @abc.abstractmethod
    def serialize(self, data: Any) -> "Repository":
        raise NotImplementedError()

    @abc.abstractmethod
    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError()

    def repository_name(self) -> str:
        return self.__class__.__name__
