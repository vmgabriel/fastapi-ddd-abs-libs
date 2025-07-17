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
    path_parameters: List[str] = pydantic.Field(default_factory=lambda: list())

    documentation: EntrypointHttpDocumentation

    def __init__(
        self,
        route: str,
        name: str,
        documentation: EntrypointHttpDocumentation,
        status_code: int = 200,
        method: model.HttpStatusType = model.HttpStatusType.GET,
        path_parameters: list[str] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if path_parameters is None:
            path_parameters = list()

        self.route = route
        self.name = name
        self.status_code = status_code
        self.method = method
        self.documentation = documentation
        self.path_parameters = path_parameters


# Default Entrypoint Documentation


class VersionNotFoundEntrypointDocumentationHttp(ExampleEntrypointDocumentationHttp):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="Error with version data",
            example_name="Error with Version",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {},
                "errors": [{"message": "Version not found", "type": "ValueError"}],
            },
        )
