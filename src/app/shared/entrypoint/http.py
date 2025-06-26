from src.app.shared import command as shared_command
from src.domain.entrypoint import http as entrypoint_http
from src.domain.entrypoint import model as entrypoint_model


class GetHealthcheckStatusExampleEntrypointDocumentationHttp(
    entrypoint_http.ExampleEntrypointDocumentationHttp
):
    def __init__(self):
        super().__init__(
            status_code=200,
            description="Basic Healthcheck Status API",
            example_name="Healthcheck V1 status",
            content={"payload": {"message": "ok"}},
        )


class GetHealthCheckStatusEntrypointHttpDocumentation(entrypoint_http.EntrypointHttpDocumentation):
    def __init__(self):
        super().__init__(
            summary="Show the Current Status of API",
            description="Get HealthCheck V1",
            responses=[GetHealthcheckStatusExampleEntrypointDocumentationHttp()],
            tags=["healthcheck"],
        )


class GetHealthcheckStatusEntrypointHttp(entrypoint_http.EntrypointHttp):
    def __init__(self):
        super().__init__(
            route="/{version}/healthcheck",
            name="Current Healthcheck Status",
            status_code=200,
            method=entrypoint_model.HttpStatusType.GET,
            documentation=GetHealthCheckStatusEntrypointHttpDocumentation(),
            security=entrypoint_model.EntrypointSecurity(),
            cmd=shared_command.HealthCheckStatusCommand(),
        )
