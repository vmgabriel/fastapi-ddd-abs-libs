import enum
from typing import Generic, TypeVar

import pydantic

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


class StatusType(enum.StrEnum):
    OK = enum.auto()
    NOT_PERMISSIONS = enum.auto()
    EXPIRED = enum.auto()
    NOT_COMPLETE = enum.auto()
    NOT_AUTHORIZED = enum.auto()


class EntrypointSecurity(pydantic.BaseModel):
    require_security: bool = False
    audiences: list[str] = pydantic.Field(default_factory=list)


class EntrypointModel(Generic[T]):
    security: EntrypointSecurity
    cmd: T

    def __init__(self, cmd: T, security: EntrypointSecurity):
        self.cmd = cmd
        self.security = security
