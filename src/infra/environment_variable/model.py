import abc
from typing import Any, Dict

from src import settings


class EnvironmentVariableAdapter(abc.ABC):
    configuration: settings.BaseSettings

    def __init__(self, configuration: settings.BaseSettings) -> None:
        self.configuration = configuration

    @abc.abstractmethod
    def get(self, key: str) -> str | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def all(self) -> Dict[str, Any]:
        raise NotImplementedError()
