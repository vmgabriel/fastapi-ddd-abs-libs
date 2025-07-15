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
                    "message": "Valid Authorization",
                    "type": "Bearer",
                    "token": "123213213213.123123123.1312312",
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
            responses=[AuthenticationEntrypointDocumentationHttp()],
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
