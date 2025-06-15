from typing import Any, Dict, List, TypeVar

import pydantic

from src.domain.services import command

from . import model

T = TypeVar("T", bound=command.Command)


class ExampleEntrypointDocumentationHttp(pydantic.BaseModel):
    status_code: int
    description: str
    example_name: str
    content: Dict[str, Any] | List[Any]
    type: model.ResponseType = model.ResponseType.JSON


class EntrypointHttpDocumentation(pydantic.BaseModel):
    summary: str
    description: str
    responses: List[ExampleEntrypointDocumentationHttp] = pydantic.Field(
        default_factory=list
    )
    tags: List[str] = pydantic.Field(default_factory=lambda: list())


class EntrypointHttp(model.EntrypointModel):
    route: str
    name: str
    status_code: int
    method: model.HttpStatusType

    documentation: EntrypointHttpDocumentation

    def __init__(
        self,
        route: str,
        name: str,
        documentation: EntrypointHttpDocumentation,
        status_code: int = 200,
        method: model.HttpStatusType = model.HttpStatusType.GET,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.route = route
        self.name = name
        self.status_code = status_code
        self.method = method
        self.documentation = documentation
