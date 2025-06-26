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
