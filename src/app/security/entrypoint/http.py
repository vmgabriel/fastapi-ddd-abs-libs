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


# Entrypoint for Generate TOKEN


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
                AuthenticationEntrypointDocumentationHttp(),
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
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
                RefreshTokenEntrypointDocumentationHttp(),
                entrypoint_http.VersionNotFoundEntrypointDocumentationHttp(),
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
