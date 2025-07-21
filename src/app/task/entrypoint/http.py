from src.app.task import command as task_commands
from src.domain.entrypoint import http as entrypoint_http
from src.domain.entrypoint import model as entrypoint_model

# Board - Create


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


# Board - Get By ID


class GetByIDBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Get Board by ID",
            example_name="Bet Board Based in ID Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-17T20:11:53.446982",
                    "updated_at": "2025-07-17T20:11:53.446988",
                    "is_activated": True,
                    "name": "Board",
                    "description": "Description of Board",
                    "icon_url": None,
                    "tasks": [],
                    "owners": ["user_id"],
                },
                "errors": [],
            },
        )


class GetByIDBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Get Board by ID",
            description="Get Board by ID",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                GetByIDBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class GetByIDBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}",
            name="Get Board By ID",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=GetByIDBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:get"],
            ),
            cmd=task_commands.GetByIDBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# Board - List


class ListBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - List Board",
            example_name="Get List Board",
            content={
                "trace_id": "505c69ac-2d61-4038-8455-6b0750b67531",
                "payload": {
                    "total": 3,
                    "page": 1,
                    "count": 1,
                    "elements": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                            "deleted_at": None,
                            "created_at": "2025-07-17T20:36:38.261728",
                            "updated_at": "2025-07-17T20:36:38.261735",
                            "is_activated": True,
                            "name": "My Chicken Board",
                            "description": "Description of My Chicken Board",
                            "icon_url": None,
                            "members": [
                                {
                                    "contact": {
                                        "email": "a@b.com",
                                        "phone": "12343443434",
                                    },
                                    "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                    "icon_url": None,
                                    "full_name": "Gabriel Vargas",
                                    "username": "vmgabriel",
                                    "role": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                                },
                                {
                                    "contact": {
                                        "email": "a@a.com",
                                        "phone": "5995959595",
                                    },
                                    "user_id": "53da7e70-fb8f-4030-b81d-ed07b2335dcb",
                                    "icon_url": None,
                                    "full_name": "aaaa aaaa",
                                    "username": "aaaa",
                                    "role": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                                },
                            ],
                            "task_summary": {
                                "total": 0,
                                "active": 0,
                                "inactive": 0,
                                "summary_status": {},
                            },
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5",
                            "deleted_at": None,
                            "created_at": "2025-07-17T20:36:38.261728",
                            "updated_at": "2025-07-17T20:36:38.261735",
                            "is_activated": True,
                            "name": "My Chicken Board",
                            "description": "Description of My Chicken Board",
                            "icon_url": None,
                            "members": [
                                {
                                    "contact": {
                                        "email": "vmgabriel96@gmail.com",
                                        "phone": "3057882366",
                                    },
                                    "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                    "icon_url": None,
                                    "full_name": "Gabriel Vargas",
                                    "username": "vmgabriel",
                                    "role": "3fa85f64-5717-4562-b3fc-2c963f66afa5",
                                }
                            ],
                            "task_summary": {
                                "total": 0,
                                "active": 0,
                                "inactive": 0,
                                "summary_status": {},
                            },
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "deleted_at": None,
                            "created_at": "2025-07-17T20:11:53.446982",
                            "updated_at": "2025-07-17T20:11:53.446988",
                            "is_activated": True,
                            "name": "My Chicken Board",
                            "description": "Description of My Chicken Board",
                            "icon_url": None,
                            "members": [
                                {
                                    "contact": {
                                        "email": "vmgabriel96@gmail.com",
                                        "phone": "3057882366",
                                    },
                                    "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                    "icon_url": None,
                                    "full_name": "Gabriel Vargas",
                                    "username": "vmgabriel",
                                    "role": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                },
                                {
                                    "contact": {
                                        "email": "a@a.com",
                                        "phone": "5995959595",
                                    },
                                    "user_id": "53da7e70-fb8f-4030-b81d-ed07b2335dcb",
                                    "icon_url": None,
                                    "full_name": "aaaa aaaa",
                                    "username": "aaaa",
                                    "role": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                },
                            ],
                            "task_summary": {
                                "total": 4,
                                "active": 4,
                                "inactive": 0,
                                "summary_status": {
                                    "done": 1,
                                    "todo": 1,
                                    "doing": 1,
                                    "abandoned": 1,
                                },
                            },
                        },
                    ],
                },
                "errors": [],
            },
        )


class ListBoardEntrypointHttpDocumentation(entrypoint_http.EntrypointHttpDocumentation):
    def __init__(self):
        super().__init__(
            summary="Get Board List",
            description="Get Board List",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                ListBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class ListBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards",
            name="Get List Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=ListBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:gets"],
            ),
            cmd=task_commands.ListBoardCommand(),
            path_parameters=["version", "query", "user"],
        )
