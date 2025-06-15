import abc
import enum

from src import settings


class DebugLevelType(enum.StrEnum):
    CRITICAL = enum.auto()
    ERROR = enum.auto()
    WARNING = enum.auto()
    INFO = enum.auto()
    NONE = enum.auto()


class LogAdapter(abc.ABC):
    configuration: settings.BaseSettings

    def __init__(self, configuration: settings.BaseSettings) -> None:
        self.configuration = configuration

    def critical(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.CRITICAL)

    def info(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.INFO)

    def warning(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.WARNING)

    def error(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.ERROR)

    @abc.abstractmethod
    def _message(self, msg: str, status: DebugLevelType) -> None:
        raise NotImplementedError()
