import enum
from typing import Generic, TypeVar

from src.domain.services import command

T = TypeVar("T", bound=command.Command)


class HttpStatusType(enum.StrEnum):
    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()


class ResponseType(enum.StrEnum):
    JSON = enum.auto()
    WS = enum.auto()


class EntrypointModel(Generic[T]):
    cmd: T

    def __init__(self, cmd: T):
        self.cmd = cmd
