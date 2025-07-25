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


# Board - Update


class UpdateBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Update Data Board",
            example_name="Update Data of Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-17T20:11:53.446982",
                    "updated_at": "2025-07-17T20:11:53.446988",
                    "is_activated": True,
                    "name": "Updated Board",
                    "description": "Updated Description of Board",
                    "icon_url": None,
                    "tasks": [],
                    "owners": ["user_id"],
                },
                "errors": [],
            },
        )


class UpdateBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Update Board",
            description="Update Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                UpdateBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class UpdateBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}",
            name="Update Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.PUT,
            documentation=UpdateBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:update"],
            ),
            cmd=task_commands.UpdateBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# Board - Delete


class DeleteBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Delete Board",
            example_name="Delete Board",
            content={
                "trace_id": "c4174093-63ad-4447-ad3e-73b04218c341",
                "payload": {
                    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": "2025-07-22T11:53:00.730519",
                    "created_at": "2025-07-22T11:52:50.441042",
                    "updated_at": "2025-07-22T11:52:50.441048",
                    "is_activated": False,
                    "name": "New Board",
                    "description": "Description of That Board",
                    "icon_url": None,
                    "tasks": [],
                    "members": [
                        {
                            "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "board_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "admin",
                        }
                    ],
                },
                "errors": [],
            },
        )


class DeleteBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Delete Board",
            description="Delete Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                DeleteBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class DeleteBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}",
            name="Delete Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.DELETE,
            documentation=DeleteBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:delete"],
            ),
            cmd=task_commands.DeleteBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# Add Member


class AddMemberBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Add Member Board",
            example_name="Add Member Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-22T17:18:58.215482",
                    "updated_at": "2025-07-22T17:18:58.215487",
                    "is_activated": True,
                    "name": "My Chicken Board",
                    "description": "Description of My Chicken Board",
                    "icon_url": None,
                    "tasks": [],
                    "members": [
                        {
                            "user_id": "53da7e70-fb8f-4030-b81d-ed07b2335dcb",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "viewer",
                        },
                        {
                            "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "admin",
                        },
                        {
                            "user_id": "05a90ad0-1053-4181-ad1c-958c1d9eacb4",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "viewer",
                        },
                    ],
                },
                "errors": [],
            },
        )


class AddMemberBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Add Member Board",
            description="Add Member Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                AddMemberBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class AddMemberBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}/members",
            name="Add Member into Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=AddMemberBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:add_member"],
            ),
            cmd=task_commands.AddMemberBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# Remove Member


class RemoveMemberBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Remove Member Board",
            example_name="Remove Member Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-22T17:18:58.215482",
                    "updated_at": "2025-07-22T17:18:58.215487",
                    "is_activated": True,
                    "name": "My Chicken Board",
                    "description": "Description of My Chicken Board",
                    "icon_url": None,
                    "tasks": [],
                    "members": [
                        {
                            "user_id": "53da7e70-fb8f-4030-b81d-ed07b2335dcb",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "viewer",
                        },
                        {
                            "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "admin",
                        },
                    ],
                },
                "errors": [],
            },
        )


class RemoveMemberBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Remove Member Board",
            description="Remove Member Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                RemoveMemberBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class RemoveMemberBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}/members/remove",
            name="Remove Member into Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=RemoveMemberBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:remove_member"],
            ),
            cmd=task_commands.RemoveMemberBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# Update RoleMember


class UpdateRoleMemberBoardEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Update Role Member Board",
            example_name="Update Role Member Board",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-22T17:18:58.215482",
                    "updated_at": "2025-07-22T17:18:58.215487",
                    "is_activated": True,
                    "name": "My Chicken Board",
                    "description": "Description of My Chicken Board",
                    "icon_url": None,
                    "tasks": [],
                    "members": [
                        {
                            "user_id": "53da7e70-fb8f-4030-b81d-ed07b2335dcb",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "editor",
                        },
                        {
                            "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "role": "admin",
                        },
                    ],
                },
                "errors": [],
            },
        )


class UpdateRoleMemberBoardEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Update Role Member Board",
            description="Update Role Member Board",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                UpdateRoleMemberBoardEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class UpdateRoleMemberBoardEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}/members/update/role",
            name="Update Role Member into Board",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=UpdateRoleMemberBoardEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["board:update_role_member"],
            ),
            cmd=task_commands.UpdateRoleMemberBoardCommand(),
            path_parameters=["version", "id", "user"],
        )


# List Task


class ListTaskEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - List Task",
            example_name="List Task",
            content={
                "trace_id": "025712b3-4be6-4999-b3ec-d1b58440d47f",
                "payload": {
                    "total": 3,
                    "page": 1,
                    "count": 3,
                    "elements": [
                        {
                            "id": "c1f9cf0f-1d35-421c-9ba0-050c280d78b3",
                            "deleted_at": None,
                            "created_at": "2025-07-20T18:05:48",
                            "updated_at": "2025-07-20T18:05:45",
                            "is_activated": True,
                            "name": "A name for a task",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "description": "A description for a task",
                            "owner": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "priority": "low",
                            "histories": [],
                            "status": "todo",
                            "icon_url": None,
                            "owner_data": {
                                "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                "username": "m",
                                "icon_id": None,
                                "full_name": "m",
                            },
                        },
                        {
                            "id": "c2f9cf0f-1d35-421c-9ba0-050c280d78b3",
                            "deleted_at": None,
                            "created_at": "2025-07-20T18:05:48",
                            "updated_at": "2025-07-20T18:05:45",
                            "is_activated": True,
                            "name": "A name for a task",
                            "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "description": "A description for a task",
                            "owner": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                            "priority": "low",
                            "histories": [],
                            "status": "doing",
                            "icon_url": None,
                            "owner_data": {
                                "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                "username": "m",
                                "icon_id": None,
                                "full_name": "m",
                            },
                        },
                    ],
                },
                "errors": [],
            },
        )


class ListTaskEntrypointHttpDocumentation(entrypoint_http.EntrypointHttpDocumentation):
    def __init__(self):
        super().__init__(
            summary="List Task",
            description="List Task",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                ListTaskEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class ListTaskEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}/tasks",
            name="Get List Tasks",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=ListTaskEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["task:gets"],
            ),
            cmd=task_commands.ListTaskCommand(),
            path_parameters=["version", "id", "query", "user"],
        )


# Create Task


class CreateTaskEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Create Task",
            example_name="Create Task",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-23T19:08:21.163963",
                    "updated_at": "2025-07-23T19:08:21.163970",
                    "is_activated": True,
                    "name": "Context",
                    "board_id": "board_id",
                    "description": "Context",
                    "owner": "user_id",
                    "priority": "high",
                    "histories": [
                        {
                            "id": "21bba247-6592-413e-972b-c90e6a46c8fa",
                            "deleted_at": None,
                            "created_at": "2025-07-23T19:08:21.163963",
                            "updated_at": "2025-07-23T19:08:21.163970",
                            "is_activated": True,
                            "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "changed_at": "2025-07-23T19:08:26.248665",
                            "type_of_change": "inserted",
                            "previous_values": None,
                            "new_values": {
                                "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "name": "Context",
                                "description": "Context",
                                "icon_url": "https://google.com/images/1.jpg",
                                "user_id": "user_id",
                                "priority": "high",
                                "board_id": "board_id",
                            },
                        }
                    ],
                    "status": "todo",
                    "icon_url": "https://google.com/images/1.jpg",
                    "owner_data": None,
                },
                "errors": [],
            },
        )


class CreateTaskEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Create Task",
            description="Create Task",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                CreateTaskEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class CreateTaskEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/boards/{id}/tasks",
            name="Create Tasks",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=CreateTaskEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["task:create"],
            ),
            cmd=task_commands.CreateTaskCommand(),
            path_parameters=["version", "id", "user"],
        )


# Get By ID - Task Detailed


class GetByIdTaskEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Get By ID Task",
            example_name="Get By ID Task",
            content={
                "trace_id": "57c8d321-2dfd-4459-a37e-4ef60da91955",
                "payload": {
                    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "deleted_at": None,
                    "created_at": "2025-07-23T19:08:21.163963",
                    "updated_at": "2025-07-23T19:08:21.163970",
                    "is_activated": True,
                    "name": "A New Task in Swagger",
                    "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                    "description": "This is Saved in Swagger Data",
                    "owner": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                    "priority": "high",
                    "histories": [
                        {
                            "id": "21bba247-6592-413e-972b-c90e6a46c8fa",
                            "deleted_at": None,
                            "created_at": "2025-07-23T19:08:21.163963",
                            "updated_at": "2025-07-23T19:08:21.163970",
                            "is_activated": True,
                            "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "changed_at": "2025-07-23T19:08:26.248665",
                            "type_of_change": "inserted",
                            "previous_values": None,
                            "new_values": {
                                "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "name": "A New Task in Swagger",
                                "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                                "icon_url": "https://google.com/images/1.jpg",
                                "priority": "high",
                                "description": "This is Saved in Swagger Data",
                            },
                        }
                    ],
                    "status": "todo",
                    "icon_url": "https://google.com/images/1.jpg",
                    "owner_data": {
                        "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                        "username": "vmgabriel",
                        "icon_id": None,
                        "full_name": "Gabriel Vargas",
                    },
                },
                "errors": [],
            },
        )


class GetByIDTaskEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Get By ID Task",
            description="Get By ID Task",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                GetByIdTaskEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class GetByIDTaskEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/tasks/{id}",
            name="Get By ID Tasks",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=GetByIDTaskEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["task:get"],
            ),
            cmd=task_commands.GetByIDTaskCommand(),
            path_parameters=["version", "id", "user"],
        )


# Update Task


class UpdateTaskEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Update Task",
            example_name="Update Task",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "payload": {
                        "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "deleted_at": None,
                        "created_at": "2025-07-23T19:08:21.163963",
                        "updated_at": "2025-07-24T09:32:33.915171",
                        "is_activated": True,
                        "name": "Updated with data",
                        "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                        "description": "Description Updated",
                        "owner": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                        "priority": "low",
                        "histories": [
                            {
                                "id": "21bba247-6592-413e-972b-c90e6a46c8fa",
                                "deleted_at": None,
                                "created_at": "2025-07-23T19:08:21.163963",
                                "updated_at": "2025-07-23T19:08:21.163970",
                                "is_activated": True,
                                "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "changed_at": "2025-07-23T19:08:26.248665",
                                "type_of_change": "inserted",
                                "previous_values": None,
                                "new_values": {
                                    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "A New Task in Swagger",
                                    "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                    "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                                    "icon_url": "https://google.com/images/1.jpg",
                                    "priority": "high",
                                    "description": "This is Saved in Swagger Data",
                                },
                            },
                            {
                                "id": "7b3f432b-0b94-475f-9f2c-105477d5673f",
                                "deleted_at": None,
                                "created_at": "2025-07-24T09:32:31.414625",
                                "updated_at": "2025-07-24T09:32:31.414630",
                                "is_activated": True,
                                "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "changed_at": "2025-07-24T09:32:33.914957",
                                "type_of_change": "updated",
                                "previous_values": {
                                    "name": "A New Task in Swagger",
                                    "description": "This is Saved in Swagger Data",
                                    "icon_url": "https://google.com/images/1.jpg",
                                    "priority": "high",
                                },
                                "new_values": {
                                    "name": "Updated with data",
                                    "description": "Description Updated",
                                    "icon_url": "https://duckduckgo.com/images/1.jpg",
                                    "priority": "low",
                                },
                            },
                        ],
                        "status": "todo",
                        "icon_url": "https://duckduckgo.com/images/1.jpg",
                        "owner_data": {},
                    },
                    "errors": [],
                },
                "errors": [],
            },
        )


class UpdateTaskEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Update Task",
            description="Update Task",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                UpdateTaskEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class UpdateTaskEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/tasks/{id}",
            name="Update Tasks",
            status_code=200,
            method=entrypoint_model.HttpStatusType.PUT,
            documentation=UpdateTaskEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["task:update"],
            ),
            cmd=task_commands.UpdateTaskCommand(),
            path_parameters=["version", "id", "user"],
        )


# Delete Task


class DeleteTaskEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 - Delete Task",
            example_name="Delete Task",
            content={
                "trace_id": "57c8d321-2dfd-4459-a37e-4ef60da91955",
                "payload": {
                    "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "payload": {
                        "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "deleted_at": None,
                        "created_at": "2025-07-23T19:08:21.163963",
                        "updated_at": "2025-07-24T09:32:33.915171",
                        "is_activated": True,
                        "name": "Updated with data",
                        "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                        "description": "Description Updated",
                        "owner": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                        "priority": "low",
                        "histories": [
                            {
                                "id": "21bba247-6592-413e-972b-c90e6a46c8fa",
                                "deleted_at": None,
                                "created_at": "2025-07-23T19:08:21.163963",
                                "updated_at": "2025-07-23T19:08:21.163970",
                                "is_activated": True,
                                "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "changed_at": "2025-07-23T19:08:26.248665",
                                "type_of_change": "inserted",
                                "previous_values": None,
                                "new_values": {
                                    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "A New Task in Swagger",
                                    "user_id": "c1f9cf0e-1d35-421c-9ba0-050c280d78b3",
                                    "board_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
                                    "icon_url": "https://google.com/images/1.jpg",
                                    "priority": "high",
                                    "description": "This is Saved in Swagger Data",
                                },
                            },
                            {
                                "id": "7b3f432b-0b94-475f-9f2c-105477d5673f",
                                "deleted_at": None,
                                "created_at": "2025-07-24T09:32:31.414625",
                                "updated_at": "2025-07-24T09:32:31.414630",
                                "is_activated": True,
                                "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "changed_at": "2025-07-24T09:32:33.914957",
                                "type_of_change": "updated",
                                "previous_values": {
                                    "name": "A New Task in Swagger",
                                    "icon_url": "https://google.com/images/1.jpg",
                                    "priority": "high",
                                    "description": "This is Saved in Swagger Data",
                                },
                                "new_values": {
                                    "name": "Updated with data",
                                    "icon_url": "https://duckduckgo.com/images/1.jpg",
                                    "priority": "low",
                                    "description": "Description Updated",
                                },
                            },
                            {
                                "id": "b1b2fbab-7e88-461e-8dd1-350d751ecc99",
                                "deleted_at": None,
                                "created_at": "2025-07-24T10:38:08.305187",
                                "updated_at": "2025-07-24T10:38:08.305193",
                                "is_activated": True,
                                "task_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "changed_at": "2025-07-24T10:38:09.870597",
                                "type_of_change": "deleted",
                                "previous_values": None,
                                "new_values": {},
                            },
                        ],
                        "status": "todo",
                        "icon_url": "https://duckduckgo.com/images/1.jpg",
                        "owner_data": {},
                    },
                    "errors": [],
                },
                "errors": [],
            },
        )


class DeleteTaskEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Delete Task",
            description="Delete Task",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                DeleteTaskEntrypointDocumentationHttp(),
            ],
            tags=["task"],
        )


class DeleteTaskEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/tasks/{id}",
            name="Delete Tasks",
            status_code=200,
            method=entrypoint_model.HttpStatusType.DELETE,
            documentation=DeleteTaskEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["task:delete"],
            ),
            cmd=task_commands.DeleteTaskCommand(),
            path_parameters=["version", "id", "user"],
        )
