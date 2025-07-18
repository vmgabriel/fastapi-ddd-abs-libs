from src.app.task import command as task_commands
from src.domain.entrypoint import http as entrypoint_http
from src.domain.entrypoint import model as entrypoint_model

# Create Board


class CreateBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Create New Board",
            example_name="Created new Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-17T20:11:53.446982",
                    "updated_at": "2025-07-17T20:11:53.446988",
                    "is_activated": True,
                    "name": "New Board",
                    "description": "Description of Board",
                    "icon_url": None,
                    "tasks": [],
                    "owners": ["user_id"],
                },
                "errors": [],
            },
        )


class CreateBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Get a Board",
            description="Based for Create Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                CreateBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class CreateBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards",
            name="Create a New Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=CreateBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:create"],
            ),
            cmd=task_commands.CreateBoardCommand(),
            path_parameters=["version", "user"],
        )
