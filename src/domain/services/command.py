import abc
import uuid
from typing import Any, Dict, List, Type, cast

import pydantic


class CommandRequest(pydantic.BaseModel):
    trace_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)


class CommandResponse(pydantic.BaseModel):
    trace_id: uuid.UUID
    payload: Dict[str, Any] = pydantic.Field(default_factory=lambda: {})
    errors: List[Dict[str, Any]] = pydantic.Field(default_factory=lambda: [])


class Command(abc.ABC):
    request_type: Type[CommandRequest]
    request: CommandRequest | None
    requirements: List[str]
    parameters: Dict[str, Any]

    _deps: Dict[str, Any]

    def __init__(
        self,
        requirements: List[str] | None = None,
        request_type: Type[CommandRequest] = CommandRequest,
    ):
        self.requirements = requirements or []
        self.request = None
        self.request_type = request_type
        self.parameters = {}

        self._deps = {}

    def inject_dependencies(self, infra_dependencies: Dict[str, Any]) -> None:
        for requirement in self.requirements:
            self._deps[requirement] = infra_dependencies[requirement]

    def inject_parameters(self, parameters: Dict[str, Any]) -> None:
        self.parameters = parameters

    def inject_request(self, request: Any) -> None:
        self.request = cast(CommandRequest, request)

    def inject_using_dict(
        self,
        request_dict: Dict[str, Any],
    ) -> None:
        self.request = self.request_type.model_validate(request_dict)

    @abc.abstractmethod
    async def execute(self) -> CommandResponse:
        raise NotImplementedError()
