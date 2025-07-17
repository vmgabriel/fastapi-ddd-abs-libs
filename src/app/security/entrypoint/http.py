from src.app.security import command as security_command
from src.domain.entrypoint import http as entrypoint_http
from src.domain.entrypoint import model as entrypoint_model


class GetDataExampleEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="Get Data with Documentation entrypoint",
            example_name="First Example",
            content={"payload": "ok"},
        )


class GetDataEntrypointHttpDocumentation(entrypoint_http.EntrypointHttpDocumentation):
    def __init__(self):
        super().__init__(
            summary="This is a summary for the documentation of entrypoint",
            description="Get Data Entrypoint",
            responses=[GetDataExampleEntrypointDocumentationHttp()],
            tags=["example"],
        )


class GetDataEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/datas",
            name="Get Datas",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=GetDataEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=security_command.GetDataCommand(),
        )


# Entrypoint for Generate and update TOKEN


class AuthenticationEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description=(
                "Based in configuration this allow to "
                "authenticate and generate access_token"
            ),
            example_name="Generate Access Token",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "status": True,
                    "message": "Valid Authorization",
                    "type": "Bearer",
                    "access_token": "aaaaa.bbbbb.cccc",
                    "refresh_token": "aaaaa.bbbbb.cccc",
                    "generation_datetime": "2025-07-15T17:31:48.923934Z",
                    "expiration_datetime": "2025-07-15T19:31:48.923934Z",
                },
                "errors": [],
            },
        )


class AuthenticationEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Based In The data for Auth generate token",
            description="Valid Authorization",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                AuthenticationEntrypointDocumentationHttp(),
            ],
            tags=["auth"],
        )


class AuthenticateEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/auth",
            name="Authenticate",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=AuthenticationEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=security_command.AuthenticateCommand(),
            path_parameters=["version"],
        )


class RefreshTokenEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description=(
                "Generates a new access token and refresh token pair "
                "using an existing valid refresh token. "
                "This endpoint allows extending authentication "
                "sessions without requiring re-authentication."
            ),
            example_name="Refresh Access Token Example",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "status": True,
                    "message": "Valid Authorization",
                    "type": "Bearer",
                    "access_token": "aaaaa.bbbbb.cccc",
                    "refresh_token": "aaaaa.bbbbb.cccc",
                    "generation_datetime": "2025-07-15T17:31:48.923934Z",
                    "expiration_datetime": "2025-07-15T19:31:48.923934Z",
                },
                "errors": [],
            },
        )


class RefreshTokenEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Refresh access token using existing refresh token",
            description="Valid Authorization",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                RefreshTokenEntrypointDocumentationHttp(),
            ],
            tags=["auth"],
        )


class RefreshTokenEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/auth/refresh",
            name="Refresh Token",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=RefreshTokenEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=security_command.RefreshAuthenticateCommand(),
            path_parameters=["version"],
        )


# Entrypoint for Create User


class CreateUserEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="Create User based in the information related to payload",
            example_name="Create User Correctly",
            content={
                "trace_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "payload": {
                    "id": "id-id-id-id-id",
                    "id_profile": "id-id-id-id-id",
                    "username": "my_username",
                },
                "errors": [],
            },
        )


class CreateUserEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Generate a basic User",
            description="Creating a User based in entrypoint",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                CreateUserEntrypointDocumentationHttp(),
            ],
            tags=["auth"],
        )


class CreateUserEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/users",
            name="Create Client Users",
            status_code=200,
            method=entrypoint_model.HttpStatusType.POST,
            documentation=CreateUserEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=security_command.CreateBasicUserCommand(),
            path_parameters=["version"],
        )


# Entrypoint for Get Profile


class GetProfileEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="V1 for Get Profile",
            example_name="Get Profile Correctly - V1",
            content={
                "trace_id": "242a3122-dc01-410c-abe9-885b9a4b2c2c",
                "payload": {
                    "id": "843d1930-9655-4df8-a564-777823c6dfce",
                    "name": "John",
                    "last_name": "Doe",
                    "username": "jhon.doe",
                    "email": "john.doe@mail.co",
                    "phone": "0123456789",
                    "icon_url": None,
                },
                "errors": [],
            },
        )


class GetProfileEntrypointHttpDocumentation(
    entrypoint_http.EntrypointHttpDocumentation
):
    def __init__(self):
        super().__init__(
            summary="Get A Profile",
            description="Based in the profile data and user get data",
            responses=[
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
                GetProfileEntrypointDocumentationHttp(),
            ],
            tags=["auth"],
        )


class GetProfileEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/users/myself",
            name="Get Profile",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=GetProfileEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(
                require_security=True,
                audiences=["profile:get"],
            ),
            cmd=security_command.GetProfileCommand(),
            path_parameters=["version", "user"],
        )
