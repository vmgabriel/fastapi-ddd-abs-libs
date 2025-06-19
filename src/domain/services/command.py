import abc
import uuid
from typing import Any, Dict, List, cast

import pydantic


class CommandRequest(pydantic.BaseModel):
    trace_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)


class CommandResponse(pydantic.BaseModel):
    trace_id: uuid.UUID
    payload: Dict[str, Any] = pydantic.Field(default_factory=lambda: {})
    errors: List[Dict[str, Any]] = pydantic.Field(default_factory=lambda: [])


class Command(abc.ABC):
    request: CommandRequest | None
    requirements: List[str]

    _deps: Dict[str, Any]

    def __init__(self, requirements: List[str] | None = None):
        self.requirements = requirements or []
        self.request = None

        self._deps = {}

    def inject_dependencies(self, infra_dependencies: Dict[str, Any]) -> None:
        for requirement in self.requirements:
            self._deps[requirement] = infra_dependencies[requirement]

    def inject_request(self, request: Any) -> None:
        self.request = cast(CommandRequest, request)

    @abc.abstractmethod
    async def execute(self) -> CommandResponse:
        raise NotImplementedError()
